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
    # template_name: ระบุเทมเพลต HTML ที่จะใช้สำหรับแสดงหน้าให้ผู้ใช้กรอกอีเมลเพื่อขอรีเซ็ตรหัสผ่าน. ในที่นี้คือ 'main/forgot_password.html'.
    template_name = 'main/forgot_password.html'
    # email_template_name: ระบุเทมเพลต HTML ที่จะใช้สำหรับอีเมลที่ส่งไปยังผู้ใช้เพื่อรีเซ็ตรหัสผ่าน. เทมเพลตนี้จะมีลิงก์สำหรับการรีเซ็ตรหัสผ่าน. ในที่นี้คือ 'main/forgot_password_email.html'.
    email_template_name = 'main/forgot_password_email.html'
    # success_url: ระบุ URL ที่จะรีไดเรกต์ผู้ใช้ไปหลังจากที่ฟอร์มรีเซ็ตรหัสผ่านถูกส่งสำเร็จ. ในที่นี้ใช้ reverse_lazy('login') เพื่อรีไดเรกต์ไปยังหน้าล็อกอิน.
    success_url = reverse_lazy('login')  

# ตั้งรหัสผ่านใหม่
class PasswordResetConfirmView(PasswordResetConfirmView):
    # template_name: ระบุเทมเพลต HTML ที่จะใช้สำหรับแสดงหน้าให้ผู้ใช้ตั้งรหัสผ่านใหม่. ในที่นี้คือ 'main/reset_password_confirm.html'.
    template_name = 'main/reset_password_confirm.html'
    # success_url: ระบุ URL ที่จะรีไดเรกต์ผู้ใช้ไปหลังจากที่รหัสผ่านใหม่ถูกตั้งสำเร็จ. ในที่นี้ใช้ reverse_lazy('login') เพื่อรีไดเรกต์ไปยังหน้าล็อกอิน.
    success_url = reverse_lazy('login')
