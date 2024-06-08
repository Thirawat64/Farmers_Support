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



# ฟังก์ชันสมัครสมาชิก
def Register(req):
    # ตรวจสอบว่าถ้า request เป็นแบบ POST
    if req.method == 'POST':
        # สร้างฟอร์ม RegisterForm และรับข้อมูลจาก req.POST
        form = RegisterForm(req.POST)
        # สร้างฟอร์ม Locations และรับข้อมูลจาก req.POST
        profile = Locations(req.POST)
        
        # ตรวจสอบว่าฟอร์มทั้งสองเป็น valid หรือไม่
        if form.is_valid() and profile.is_valid():
            # บันทึกฟอร์มผู้ใช้ (RegisterForm) แต่ยังไม่บันทึกลงฐานข้อมูล (commit=False)
            user = form.save(commit=False)
            # บันทึกฟอร์มข้อมูลโปรไฟล์ (Locations) แต่ยังไม่บันทึกลงฐานข้อมูล (commit=False)
            profile_data = profile.save(commit=False)
            # กำหนดผู้ใช้ให้กับโปรไฟล์
            profile_data.user = user
            # บันทึกผู้ใช้ลงฐานข้อมูล
            user.save()
            # บันทึกข้อมูลโปรไฟล์ลงฐานข้อมูล
            profile_data.save()
            
            # เปลี่ยนเส้นทางไปยังหน้า login
            return redirect('login')
    else:
        # ถ้า request ไม่ใช่แบบ POST สร้างฟอร์มเปล่าทั้งสองฟอร์ม
        form = RegisterForm()
        profile = Locations()

    # ส่งฟอร์มไปยังเทมเพลต register.html
    return render(req, 'users/register.html', {'form': form, 'profile': profile})



#ล็อกอิน
def Login(req):
    return render(req, 'registration/login.html')


# ฟังก์ชันหน้าแดชบอร์ด
@login_required
def dashboard(req):
    # ดึงข้อมูลการขายที่ผู้ใช้ปัจจุบันเป็นเจ้าของ
    sell = Sell_Buy.objects.filter(user=req.user)
    # ดึงข้อมูลสินค้าที่ผู้ใช้ปัจจุบันเป็นเจ้าของ
    buy = AllProduct.objects.filter(user=req.user)
    # ส่งข้อมูลการขายและการซื้อไปยังเทมเพลต dashboard.html
    return render(req, 'users/dashboard.html', {'sell': sell, 'buy': buy})



#เพิ่มโปรไฟล์
# ฟังก์ชันเพิ่มโปรไฟล์
def add_profile(request):
    # สร้างฟอร์มเปล่าสำหรับ EditForm และ Locations
    form = EditForm()
    profile = Locations()

    # ตรวจสอบว่าถ้า request เป็นแบบ POST
    if request.method == 'POST':
        # สร้างฟอร์ม Locations และรับข้อมูลจาก request.POST
        profile = Locations(request.POST)
        # สร้างฟอร์ม EditForm โดยใช้ข้อมูลจาก request.POST และกำหนด instance เป็นผู้ใช้ปัจจุบัน
        form = EditForm(request.POST, instance=request.user)

        # ตรวจสอบว่าฟอร์มทั้งสองเป็น valid หรือไม่
        if form.is_valid() and profile.is_valid():
            # บันทึกฟอร์มข้อมูลโปรไฟล์ (Locations) แต่ยังไม่บันทึกลงฐานข้อมูล (commit=False)
            profile_data = profile.save(commit=False)
            # กำหนดผู้ใช้ให้กับโปรไฟล์
            profile_data.user = request.user
            # บันทึกข้อมูลโปรไฟล์ลงฐานข้อมูล
            profile_data.save()
            # บันทึกฟอร์มผู้ใช้ลงฐานข้อมูล
            form.save()
            # เปลี่ยนเส้นทางไปยังหน้าแดชบอร์ด
            return redirect('dashboard')
        else:
            # ถ้าฟอร์มไม่ valid สร้างฟอร์มเปล่าทั้งสองฟอร์มใหม่
            form = EditForm()
            profile = Locations()

    else:
        # ถ้า request ไม่ใช่แบบ POST สร้างฟอร์ม EditForm โดยมี instance เป็นผู้ใช้ปัจจุบัน
        form = EditForm(instance=request.user)
        # สร้างฟอร์ม Locations เปล่า
        profile = Locations()

    # ส่งฟอร์มไปยังเทมเพลต add_profile.html พร้อมกับ context ที่มีตัวแปร form และ profile
    return render(request, 'users/add_profile.html', {'form': form, 'profile': profile})


# ฟังก์ชันแก้ไขโปรไฟล์
def editprofile(request):
    # ดึงข้อมูลโปรไฟล์ของผู้ใช้ปัจจุบัน
    p = User_profile.objects.get(user=request.user)
    # สร้างฟอร์ม Locations โดยมี instance เป็นโปรไฟล์ของผู้ใช้ปัจจุบัน
    profile = Locations(instance=p)
    # สร้างฟอร์ม EditForm โดยมี instance เป็นผู้ใช้ปัจจุบัน
    form = EditForm(instance=request.user)

    if request.method == 'POST':
        # ถ้า request เป็นแบบ POST สร้างฟอร์ม Locations และ EditForm ใหม่โดยรับข้อมูลจาก request.POST
        profile = Locations(request.POST, instance=p)
        form = EditForm(request.POST, instance=request.user)

        # ตรวจสอบว่าฟอร์มทั้งสองเป็น valid หรือไม่
        if form.is_valid() and profile.is_valid():
            # บันทึกฟอร์มข้อมูลโปรไฟล์ (Locations) แต่ยังไม่บันทึกลงฐานข้อมูล (commit=False)
            profile_data = profile.save(commit=False)
            # กำหนดผู้ใช้ให้กับโปรไฟล์
            profile_data.user = request.user
            # บันทึกข้อมูลโปรไฟล์ลงฐานข้อมูล
            profile_data.save()
            # บันทึกฟอร์มผู้ใช้ลงฐานข้อมูล
            form.save()
            # เปลี่ยนเส้นทางไปยังหน้าแดชบอร์ด
            return redirect('dashboard')
        else:
            # ถ้าฟอร์มไม่ valid สร้างฟอร์มเปล่าทั้งสองฟอร์มใหม่
            form = EditForm()
            profile = Locations()

    else:
        # ถ้า request ไม่ใช่แบบ POST สร้างฟอร์ม EditForm โดยมี instance เป็นผู้ใช้ปัจจุบัน
        form = EditForm(instance=request.user)
        # สร้างฟอร์ม Locations โดยมี instance เป็นโปรไฟล์ของผู้ใช้ปัจจุบัน
        profile = Locations(instance=p)

    # ส่งฟอร์มไปยังเทมเพลต edit_profile.html พร้อมกับ context ที่มีตัวแปร form และ profile
    return render(request, 'users/edit_profile.html', {'form': form, 'profile': profile})


# ฟังก์ชันแก้ไขหน้าเช่า
def Edit_sell_product(req):
    # ดึงข้อมูลสินค้าที่ผู้ใช้ปัจจุบันเป็นเจ้าของ และนับจำนวนการขายที่ยังไม่ได้อ่าน
    sell = AllProduct.objects.filter(user=req.user).annotate(unread_sells_count=Count('sells', filter=Q(sells__read=False)))
    # วนลูปผ่านแต่ละสินค้าใน sell และพิมพ์จำนวนการขายที่ยังไม่ได้อ่าน
    for i in sell:
        print(i.sells.filter(read=False).count())
    # ส่งข้อมูลสินค้าไปยังเทมเพลต edit_sell_product.html
    return render(req, 'users/edit_sell_product.html', {'sell': sell})

# ฟังก์ชันแก้ไขหน้าปล่อยเช่า
def view_rental_history(req):
    # ดึงข้อมูลการเช่าที่ผู้ใช้ปัจจุบันเป็นเจ้าของ
    buy = Sell_Buy.objects.filter(user=req.user)
    # ส่งข้อมูลการเช่าไปยังเทมเพลต view_rental_history.html
    return render(req, 'users/view_rental_history.html', {'buy': buy})

# ฟังก์ชันลบหน้าปล่อยเช่า
def delete_sell(req, id):
    # พิมพ์ค่า id ออกมา (สำหรับการดีบัก)
    print(id)
    # ดึงข้อมูลของ AllProduct ที่มี primary key เท่ากับ id และลบออบเจ็กต์นั้นออกจากฐานข้อมูล
    AllProduct.objects.get(pk=id).delete()
    # เปลี่ยนเส้นทางไปยังเส้นทาง /user/Edit_sell_product/
    return redirect('/user/Edit_sell_product/')

# ฟังก์ชันลบของในหน้าเช่า
def delete_buy(req, id):
    # พิมพ์ค่า id ออกมา (สำหรับการดีบัก)
    print(id)
    # ดึงข้อมูลของ Sell_Buy ที่มี primary key เท่ากับ id และลบออบเจ็กต์นั้นออกจากฐานข้อมูล
    Sell_Buy.objects.get(pk=id).delete()
    # เปลี่ยนเส้นทางไปยังเส้นทาง /user/view_rental_history/
    return redirect('/user/view_rental_history/')

# ฟังก์ชันดูรายละเอียดผู้มาเช่า
def See_rentals_product(req, id):
    # ดึงข้อมูลของ AllProduct ที่มี primary key เท่ากับ id มาเก็บในตัวแปร pro
    pro = AllProduct.objects.get(pk=id)
    # ดึงข้อมูลของ Sell_Buy ที่ตรงกับสินค้า pro
    users = Sell_Buy.objects.filter(product=pro)
    # วนลูปผ่านแต่ละผู้ใช้ใน users และเปลี่ยนสถานะการอ่านเป็น True
    for i in users:
        i.read = True
        i.save()
    # ส่งข้อมูลผู้ใช้และข้อมูลจังหวัดไปยังเทมเพลต See_rentals_product.html
    return render(req, 'users/See_rentals_product.html', {'users': users, 'provinces': Provinces.objects.all()})




