from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User_profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name='Profile')
    email = models.EmailField(max_length = 50)
    locations = models.CharField(max_length = 100)
    phon_numbers = models.CharField(max_length = 10)