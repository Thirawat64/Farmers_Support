from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from user.models import User_profile
from django.contrib.auth.forms import PasswordChangeForm

# ฟอร์มสมัครสมาชิก
class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # กำหนดฟิลด์ให้ฟอร์มรวมฟิลด์จาก UserCreationForm และเพิ่มฟิลด์ 'email'
        fields = UserCreationForm.Meta.fields + ('email',)

# ฟอร์มแก้ไขผู้ใช้
class EditForm(forms.ModelForm):
    class Meta:
        model = User
        # กำหนดฟิลด์ที่ต้องการใช้ในฟอร์ม ได้แก่ 'first_name', 'last_name', และ 'email'
        fields = ['first_name', 'last_name', 'email']

# ฟอร์มข้อมูลโปรไฟล์
class Locations(forms.ModelForm):
    class Meta:
        model = User_profile
        # กำหนดฟิลด์ที่ต้องการใช้ในฟอร์ม ได้แก่ 'locations' และ 'phon_numbers'
        fields = ['locations', 'phon_numbers']

        # กำหนด label ให้กับฟิลด์ในฟอร์ม
        labels = {
            'locations': "ที่อยู่",
            'phon_numbers': "เบอร์โทรศัพท์",
        }

        # กำหนด widget สำหรับฟิลด์ 'locations'
        widgets = {
            'locations': forms.Textarea(attrs={'class': 'emailinput py-2 leading-normal px-4 rounded-lg block bg-white appearance-none border w-full text-gray-700 border-gray-300 focus:outline-none'})
        }

# ฟอร์มเปลี่ยนรหัสผ่าน
class CustomPasswordChangeForm(PasswordChangeForm):
    pass

    pass

