from django.forms import ModelForm
from django import forms
from .models import *

class Search1(forms.Form):
    search = forms.CharField(label='Search')
  


class UploadForm(forms.ModelForm):
    class Meta:
        model = AllProduct
        fields = '__all__'

class Update(forms.ModelForm):
    class Meta:
        model = AllProduct
        fields = '__all__'


