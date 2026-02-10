# File: myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # This line is the bridge! It connects the main project to your home app.
    path('api/', include('home.urls')), 
]