from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from user.models import User_profile
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields +('email',) 
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("มีผู้ใช้อีเมลนี้ไปแล้ว")
        return email
        
        

class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class Locations(forms.ModelForm):
    class Meta:
        model = User_profile
        fields = ['locations','phon_numbers']
        labels = {
            'locations':"ที่อยู่",
            'phon_numbers':"เบอร์โทรศัพท์",
        }

        widgets = {
            'locations':forms.Textarea(attrs={'class':'emailinput py-2 leading-normal px-4 rounded-lg block bg-white appearance-none border w-full text-gray-700 border-gray-300 focus:outline-none'}),
            'phon_numbers':forms.TextInput(attrs={'class':'h-10 emailinput py-2 leading-normal px-4 rounded-lg block bg-white appearance-none border w-full text-gray-700 border-gray-300 focus:outline-none'})
        }

        labels = {
            'locations':"ที่อยู่",
            'phon_numbers':"เบอร์โทรศัพท์",
        }

        widgets = {
            'locations':forms.Textarea(attrs={'class':'emailinput py-2 leading-normal px-4 rounded-lg block bg-white appearance-none border w-full text-gray-700 border-gray-300 focus:outline-none'})
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    pass

