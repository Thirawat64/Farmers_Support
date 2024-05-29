from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import logout


from django.shortcuts import render,redirect

# Create your views here.

def Home(req):
    return render(req, 'main/home.html')

def About(req):
    return render(req, 'main/about.html')

def Help(req):
    return render(req, 'main/help.html')

def contact(req):
    return render(req, 'main/detall_contact.html')

def Logout(request):
    logout(request)
    return redirect('/')

#ลิมพาสเวิด
class ForgotPasswordView(PasswordResetView):
    template_name = 'main/forgot_password.html'
    email_template_name = 'main/forgot_password_email.html'
    success_url = reverse_lazy('login')  

#ตั้งรหัสผ่านใหม่
class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'main/reset_password_confirm.html'
    success_url = reverse_lazy('login')