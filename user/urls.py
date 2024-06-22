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
    path('dashboard/',view=views.dashboard , name='dashboard'),
    path('editprofile/',view=views.editprofile , name='editprofile'),
    # path('add_profile/',view=views.add_profile , name='add_profile'),
    path('view_rental_history/', view_rental_history, name='view_rental_history'),
    path('Edit_sell_product/',view=views.Edit_sell_product , name='Edit_sell_product'),
    # path('edit/Allproduct/<int:id>/',view=views.update_product,name='edit_product'),
    path('delete_sell/<int:id>/',delete_sell, name="delete_sell"),
    path('delete_buy/<int:id>/',delete_buy, name="delete_buy"),
    path('See_rentals_product/<int:id>/',See_rentals_product, name="See_rentals_product"),


    

    

    # You can include more authentication-related URLs as needed
    # path('password_reset/', include('django.contrib.auth.urls')),
]
