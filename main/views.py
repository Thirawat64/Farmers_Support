
from django.shortcuts import render

# Create your views here.

def Home(req):
    return render(req, 'main/home.html')

def About(req):
    return render(req, 'main/about.html')

def Help(req):
    return render(req, 'main/help.html')

def contact(req):
    return render(req, 'main/detall_contact.html')