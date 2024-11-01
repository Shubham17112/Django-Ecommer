from django.shortcuts import render, redirect
from ecommerceApp.forms import ContactForm
from .models import Contact
from django.contrib import messages
from .models import Category
from .models import Product, CartItem



from django.http import HttpResponse




def Home(request):
    categories = Category.objects.all()
    products = Product.objects.all()# Fetch all categories from the database
    return render(request, 'index.html', {'categories': categories,'products': products,}) 

def index(request):
    
	return render(request, 'base.html')



def cart(request):
    total_prize = sum(item.product.prize * item.quantity)
    return render(request,'cart.html')


def add_to_cart(request,product_id):
    if request.user.is_authenticated:
        product = Product.objects.get( id =  product_id)
        cart_item, created = CartItem.objects.get_or_create( product=product, user=request.user )
        cart_item.quantity += 1
        cart_item.save()
        return redirect("Home")
    else:
       return redirect('login')
   



    


def category_products(request,category_id=None):
    if category_id:
       
        category = Category.objects.filter(id = category_id).first()
        products = Product.objects.filter(category =  category)
        
    # else:
    #    hello='this is else statemetn'
    #    products = Product.objects.all()
    categories = Category.objects.all()
  

    return render(
        request,'index.html',
       
        {
        'category': category,
        'categories': categories,
        'products': products,
       
        
        }
    )
       
        

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            Contact.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            messages.info(request, "Your Data has been  successfully  sended we will contact within 24hr")

            return redirect('/contact/')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

