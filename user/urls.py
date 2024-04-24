from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import *
from . import views



urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    # Your other views and paths go here
    path('register/',view=views.Register , name='register'),
    #path('login/', Login, name='login'),
    # Example: Include Django authentication URLs
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/',view=views.dashboard , name='dashboard'),
    path('editprofile/',view=views.editprofile , name='editprofile'),
    
    

    

    # You can include more authentication-related URLs as needed
    path('password_reset/', include('django.contrib.auth.urls')),
]
