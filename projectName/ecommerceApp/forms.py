from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Enter your name',
    }))
    email = forms.EmailField(label='Your Email', widget=forms.EmailInput(attrs={
        'class': 'form-input',
        'placeholder': 'Enter your email',
    }))
    message = forms.CharField(label='Your Message', widget=forms.Textarea(attrs={
        'class': 'form-input',
        'placeholder': 'Write your message here',
        'rows': 4,
    }))
