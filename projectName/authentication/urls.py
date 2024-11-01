
# Import necessary modules
from django.contrib import admin  # Django admin module
from django.urls import path  , include
from django.conf.urls.static import static  # Import static function for serving media files
from . import views

from django.conf import settings   # Application settings
# URL routing
from authentication.views import *  # Import views from the authentication app
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # Static files serving

# Define URL patterns
urlpatterns = [
     # Home page
    path('',Home, name='Home'), 
    path("admin/", admin.site.urls),          # Admin interface
    path('logout/', views.logout_view, name='logout'),
    path('login/', login_page, name='login'),    # Login page
    path('register/', register_page, name='register'),  # Registration page
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    
]

# Serve media files if DEBUG is True (development mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files using staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()