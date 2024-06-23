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



# แก้ไขโปรไฟล์
def editprofile(request):
    # ดึงข้อมูลโปรไฟล์ของผู้ใช้ที่เข้าสู่ระบบ
    p = User_profile.objects.get(user=request.user)
    # สร้างฟอร์ม Locations และ EditForm โดยใส่ข้อมูลเริ่มต้นจากโปรไฟล์และผู้ใช้ปัจจุบัน
    profile = Locations(instance=p)
    form = EditForm(instance=request.user)

    if request.method == 'POST':
        # ถ้า request เป็น POST แสดงว่ามีการส่งฟอร์มมา
        profile = Locations(request.POST, instance=p)
        form = EditForm(request.POST, instance=request.user)

        if form.is_valid() and profile.is_valid():
            # ถ้าฟอร์มทั้งสองฟอร์มถูกต้อง
            profile.save(commit=False).user = request.user
            profile.save()
            form.save()
            return redirect('dashboard')
        else:
            form = EditForm()
            profile = Locations()
    else:
        # ถ้า request ไม่ใช่ POST ให้สร้างฟอร์มใหม่จากข้อมูลผู้ใช้และโปรไฟล์ปัจจุบัน
        form = EditForm(instance=request.user)
        profile = Locations(instance=p)

    return render(request, 'users/edit_profile.html', {'form': form, 'profile': profile})

# หน้าเช่า
def Edit_sell_product(req):
    # ดึงข้อมูลสินค้าที่ผู้ใช้ปล่อยเช่า พร้อมนับจำนวนการเช่าที่ผู้ใช้ยังไม่ได้อ่าน
    sell = AllProduct.objects.filter(user=req.user).annotate(unread_sells_count=Count('sells', filter=Q(sells__read=False)))
    for i in sell:
        print(i.sells.filter(read=False).count())
    return render(req, 'users/edit_sell_product.html', {'sell': sell})

# หน้าปล่อยเช่า
def view_rental_history(req):
    # ดึงข้อมูลการเช่าทั้งหมดของผู้ใช้ที่เข้าสู่ระบบ
    buy = Sell_Buy.objects.filter(user=req.user)
    return render(req, 'users/view_rental_history.html', {'buy': buy})

# ลบหน้าปล่อยเช่า
def delete_sell(req, id):
    print(id)
    AllProduct.objects.get(pk=id).delete()  # ลบสินค้าที่ปล่อยเช่า
    return redirect('/user/Edit_sell_product/')

# ลบของในหน้าเช่า
def delete_buy(req, id):
    print(id)
    sell_buy_instance = Sell_Buy.objects.get(pk=id)  # ดึงข้อมูลการเช่าที่ต้องการลบ
    product = sell_buy_instance.product  # ดึงสินค้าที่เกี่ยวข้องกับการเช่า
    
    product.quantity += 1  # เพิ่มจำนวนสินค้ากลับคืน
    product.save()  # บันทึกการเปลี่ยนแปลง
    
    sell_buy_instance.delete()  # ลบการเช่าออกจากฐานข้อมูล
    
    return redirect('/user/view_rental_history/')

# ดูรายละเอียดผู้มาเช่า
@login_required
def See_rentals_product(req, id):
    pro = get_object_or_404(AllProduct, pk=id)  # ดึงข้อมูลสินค้าที่ปล่อยเช่าตาม ID
    users = Sell_Buy.objects.filter(product=pro)  # ดึงข้อมูลการเช่าทั้งหมดที่เกี่ยวข้องกับสินค้า
    for i in users:
        i.read = True  # ตั้งค่าสถานะการเช่าเป็นอ่านแล้ว
        i.save()

    return render(req, 'users/see_rentals_product.html', {
        'users': users,
        'provinces': Provinces.objects.all(),
        'product': pro
    })





