
from django.urls import path
from . import views  # Import the views from views.py

urlpatterns=[
      path('', views.Home, name='Home'), 
      path('cart/', views.cart, name='cart'),  # View by category

      path('contact/',views.contact,name='contact'),
      path('<int:category_id>/', views.category_products, name='category_products'),  # View by category
   path('cart:<int:product_id>/', views.add_to_cart, name='add_to_cart'),
   ]
