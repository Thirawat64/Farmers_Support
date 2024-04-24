from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from user.models import User_profile

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        
        fields = UserCreationForm.Meta.fields +('email',) 

class EditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class Locations(UserChangeForm):
    class Meta:
        model = User_profile
        fields = ['locations','phon_numbers']

