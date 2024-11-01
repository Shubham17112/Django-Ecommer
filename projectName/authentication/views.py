from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str 
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from .utils import account_activation_token
from django.contrib.auth import get_user_model


def Home(request):
    return render(request,'index.html')

# Define a view function for the login page
def login_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/login/')
        
        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)
        
        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            return redirect('Home')
    
    # Render the login page template (GET request)
    return render(request, 'login.html')

# Define a view function for the registration page
def register_page(request):
    
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'register.html')  
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
        
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('/register/')
        
        # Create a new User object with the provided information
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
            
        )
        # Call the send_verification_email function with request and user_data
        # inactive_user = send_verification_email(request, user)              
       
        # Set the user's password and save the user object
        user.is_active = False 
         # Generate email verification token
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Build the activation link
        activation_link = request.build_absolute_uri(f'/activate/{uid}/{token}/')
        subject = 'Activate Your Account'
        message = render_to_string('email_verification.html', {
            'user': user,
            'activation_link': activation_link,
        })
        send_mail(subject, message, 'noreply@yourdomain.com', [user.email])
        user.set_password(password)
        user.save()
        
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully! We sended login link")

            # Redirect to login or any other page
        return redirect('/register/')
        
    
    # Render the registration page template (GET request)
    return render(request, 'register.html')
User = get_user_model()

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # Use force_str here as well
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('/login/')
    else:
        messages.error(request, 'The activation link is invalid!')
        return redirect('/register/')
    
# Example view function for logging out
def logout_view(request):
    # Clear the session
    request.session.flush()  # Removes all session data
    
    return redirect('login')  # Redirect to login or another page after logout
    