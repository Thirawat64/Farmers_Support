from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name='home'),
    path('about/', About, name='about'),
    path('help/', Help, name='help'),
    path('contact/', contact, name='contact'),
    path('logout/', Logout, name='Logout'),

    path('password_reset/', ForgotPasswordView.as_view()),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirms'),
]