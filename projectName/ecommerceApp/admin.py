from django.contrib import admin
from .models import Contact
from .models import Product,CartItem

from .models import Category

admin.site.register(Contact)
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CartItem)
