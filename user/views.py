from django.contrib.auth.decorators import login_required
from audioop import reverse
from django.contrib.auth import login,logout
from django.shortcuts import render , redirect ,get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect
from user.forms import  RegisterForm
from django.contrib import messages
from .forms import *
from shop.models import *
from shop.forms import Update
from django.db.models import Count, Q



#สมัครสมาชิก
def Register(req):
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        profile = Locations(req.POST)

        
        if form.is_valid() and profile.is_valid():  
            form.save(commit=False)
            profile.save(commit=False).user = form.save(commit=False)
            form.save()
            profile.save()
            
  
            return redirect('login')  
    else:
        form = RegisterForm()
        profile = Locations(req.POST)

    return render(req, 'users/register.html',{'form': form,'profile': profile})
#password non12345678

#ล็อกอิน
def Login(req):
    return render(req, 'registration/login.html')


#หน้าแดสบอด
@login_required
def dashboard(req):
    sell = Sell_Buy.objects.filter(user=req.user)
    buy = AllProduct.objects.filter(user=req.user)
    return render(req, 'users/dashboard.html',{'sell':sell,'buy':buy})


#เพิ่มโปรไฟล์
def add_profile(request):
    form = EditForm()
    profile = Locations()


    if request.method == 'POST':
        profile = Locations(request.POST)
        form = EditForm(request.POST,instance=request.user)

        if form.is_valid() and profile.is_valid():
            profile.save(commit=False).user = request.user ######ใช้ระบุผู้ใช้
            profile.save()
            form.save()
            return redirect('dashboard')
        else:
            form = EditForm()
            profile = Locations()

    else:
        form = EditForm(instance=request.user)
        profile = Locations()

    return render(request,'users/add_profile.html',{'form':form,'profile':profile ,})

#แก้ไขโปรไฟล์
def editprofile(request):
    p = User_profile.objects.get(user=request.user)
    profile = Locations(instance=p)
    form = EditForm(instance=request.user)

    if request.method == 'POST':
        profile = Locations(request.POST,instance=p)
        form = EditForm(request.POST,instance=request.user)

        if form.is_valid() and profile.is_valid():
            profile.save(commit=False).user = request.user
            profile.save()
            form.save()
            return redirect('dashboard')
        else:
            form = EditForm()
            profile = Locations()

    else:
        form = EditForm(instance=request.user)
        profile = Locations(instance=p)


    return render(request,'users/edit_profile.html',{'form':form,'profile':profile})

#แก้ไขหน้าเช่า
def Edit_sell_product(req):
    sell = AllProduct.objects.filter(user=req.user).annotate(unread_sells_count=Count('sells', filter=Q(sells__read=False)))
    for i in sell:
        print(i.sells.filter(read=False).count())
    return render(req, 'users/edit_sell_product.html',{'sell':sell})

#แก้ไขหน้าปล่อยเช่า
def view_rental_history(req):
    buy = Sell_Buy.objects.filter(user=req.user)
    return render(req, 'users/view_rental_history.html',{'buy':buy})


#ลบหน้าปล่อยเช่า
def delete_sell(req, id):
    print(id)
    AllProduct.objects.get(pk=id).delete()
    return redirect('/user/Edit_sell_product/')

#ลบของในหน้าเช่าา
def delete_buy(req, id):
    print(id)
    Sell_Buy.objects.get(pk=id).delete()
    return redirect('/user/view_rental_history/')

#ดูรายละเอียดผู้มาเช้า
def See_rentals_product(req,id):
    pro = AllProduct.objects.get(pk=id)
    users = Sell_Buy.objects.filter(product=pro)
    for i in users:
        i.read = True
        i.save()

    return render(req, 'users/See_rentals_product.html',{'users':users,'provinces': Provinces.objects.all()})



