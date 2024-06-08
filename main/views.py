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

# ลืมรหัสผ่าน
class ForgotPasswordView(PasswordResetView):
    # กำหนดเทมเพลตสำหรับหน้า Forgot Password
    template_name = 'main/forgot_password.html'
    # กำหนดเทมเพลตสำหรับอีเมล Forgot Password
    email_template_name = 'main/forgot_password_email.html'
    # กำหนดเส้นทางที่จะเปลี่ยนไปหลังจากส่งคำขอสำเร็จ
    success_url = reverse_lazy('login')  

# ตั้งรหัสผ่านใหม่
class PasswordResetConfirmView(PasswordResetConfirmView):
    # กำหนดเทมเพลตสำหรับหน้าตั้งรหัสผ่านใหม่
    template_name = 'main/reset_password_confirm.html'
    # กำหนดเส้นทางที่จะเปลี่ยนไปหลังจากตั้งรหัสผ่านใหม่สำเร็จ
    success_url = reverse_lazy('login')
