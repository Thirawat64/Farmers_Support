from django.contrib.auth.decorators import login_required
from audioop import reverse
from django.contrib.auth import login,logout
from django.shortcuts import render , redirect
from django.http import HttpRequest, HttpResponseRedirect
from user.forms import  RegisterForm
from django.contrib import messages
from .forms import *
from shop.models import *
from shop.forms import Update
from django.db.models import Count, Q



# Create your views here.
def Register(req):
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(req, f'คุณ {username} สมัครสามชิกสำเร็จ')
            return redirect('login')  
    else:
        form = RegisterForm()
    return render(req, 'users/register.html',{'form': form})
#password non12345678

def Login(req):
    return render(req, 'registration/login.html')



@login_required
def dashboard(req):
    sell = Sell_Buy.objects.filter(user=req.user)
    buy = AllProduct.objects.filter(user=req.user)
    return render(req, 'users/dashboard.html',{'sell':sell,'buy':buy})

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


def Edit_sell_product(req):
    sell = AllProduct.objects.filter(user=req.user).annotate(unread_sells_count=Count('sells', filter=Q(sells__read=False)))
    for i in sell:
        print(i.sells.filter(read=False).count())
    return render(req, 'users/edit_sell_product.html',{'sell':sell})

def Edit_buy_product(req):
    buy = Sell_Buy.objects.filter(user=req.user)
    # print(buy)
    
    # context = Edit_buy_product
    return render(req, 'users/edit_buy_product.html',{'buy':buy})

# def update_product(req, id):
#     provinces = Provinces.objects.all()
#     categories = Category.objects.all()
#     statuses = Status.objects.all()
#     c = AllProduct.objects.get(pk=id)
#     form = Update(instance=c)

#     if req.method == 'POST':
#         form = Update(req.POST,req.FILES, instance=c)
#         if form.is_valid():
#             form.save(commit=False).user = req.user
#             form.save()
#             return redirect('/user/Edit_sell_product/')
#     else:
#         form = Update(instance=c)

#     return render(req, 'users/edit_product.html', {'form': form, 'c': c, 'categories': categories, 'status': statuses ,'provinces':provinces})



def delete_sell(req, id):
    print(id)
    AllProduct.objects.get(pk=id).delete()
    return redirect('/user/Edit_sell_product/')

def delete_buy(req, id):
    print(id)
    AllProduct.objects.get(pk=id).delete()
    return redirect('/user/Edit_buy_product/')

def See_rentals_product(req,id):
    pro = AllProduct.objects.get(pk=id)
    users = Sell_Buy.objects.filter(product=pro)
    for i in users:
        i.read = True
        i.save()

    return render(req, 'users/See_rentals_product.html',{'users':users,'provinces': Provinces.objects.all()})



