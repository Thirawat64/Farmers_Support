from django.forms import ModelForm
from django import forms
from .models import *

class Search1(forms.Form):
    search = forms.CharField(label='Search')
  


class UploadForm(forms.ModelForm):
    class Meta:
        model = AllProduct
        fields = '__all__'
        exclude = ['user']

        labels = {
            'product_name':"ชื่อสินค้า",
            'phon_number':"เบอร์โทรศัพท์",
            'product_price':"ราคา",
            'product_detail':"รายละเอียด",
            'product_size':"ขนาด",
            'product_status':"สถานะ",
            'category':"ประเภท",
            'province':"จังหวัด",
            'product_location':"ที่อยู่",
            'image':"รูปภาพ",
            'datetime':"วันปล่อยเช่า",
            'lastdate':"สิ้นสุดวันปล่อยเช่า",
            'quantity':"จำนวน",
        }

        widgets = {
            'datetime':forms.DateInput(attrs={'type':'date'}),
            'lastdate':forms.DateInput(attrs={'type':'date'}),
            }

class EditForm(forms.ModelForm):
    class Meta:
        model = AllProduct
        fields = '__all__'
        exclude = ['user']

        labels = {
            'product_name':"ชื่อสินค้า",
            'phon_number':"เบอร์โทรศัพท์",
            'product_price':"ราคา",
            'product_detail':"รายละเอียด",
            'product_size':"ขนาด",
            'product_status':"สถานะ",
            'category':"ประเภท",
            'province':"จังหวัด",
            'product_location':"ที่อยู่",
            'image':"รูปภาพ",
            'datetime':"วันปล่อยเช่า",
            'lastdate':"สิ้นสุดวันปล่อยเช่า",
            'quantity':"จำนวน",
            
        }

        widgets = {
            'datetime': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'lastdate': forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'),
        }



class Update(forms.ModelForm):
    class Meta:
        model = AllProduct
        fields = '__all__'


