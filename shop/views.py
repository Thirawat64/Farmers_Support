from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,render,redirect,HttpResponseRedirect
from .models import * 
from .forms import *
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone


#ค้นหา

def searches(req):
    # ดึงออบเจ็กต์ทั้งหมดจาก AllProduct และ Category มาไว้ในตัวแปร
    show_product = AllProduct.objects.all()  # ดึงข้อมูลสินค้าทั้งหมดจากฐานข้อมูล
    categorys = Category.objects.all()  # ดึงข้อมูลหมวดหมู่สินค้าทั้งหมดจากฐานข้อมูล
    expired_products = []  # สร้างลิสต์ว่างเพื่อเก็บ ID ของสินค้าที่หมดอายุ

    if req.method == 'POST':
        # ถ้า request method เป็น POST
        search = req.POST.get('search')  # รับค่าคำค้นหาจากฟอร์ม
        print(search)  # แสดงค่าคำค้นหาที่รับมาใน console (สำหรับการดีบัก)
        if search:
            # ถ้ามีการระบุคำค้นหา
            show_product = AllProduct.objects.filter(product_name__icontains=search) or AllProduct.objects.filter(product_location__icontains=search)
            # ค้นหาสินค้าที่มีชื่อหรือที่ตั้งที่ตรงกับคำค้นหา (case-insensitive)
        else:
            # ถ้าไม่มีการระบุคำค้นหา
            show_product = AllProduct.objects.all()  # ดึงข้อมูลสินค้าทั้งหมดจากฐานข้อมูล
    else:
        # ถ้า request method ไม่ใช่ POST
        form = Search1()  # สร้างฟอร์มค้นหาใหม่

    for product in show_product:
        # วนลูปเช็คสินค้าทุกตัวใน show_product
        if product.lastdate and product.lastdate < timezone.now().date():
            # ถ้าสินค้ามีวันที่สิ้นสุดการเช่า (lastdate) และวันที่นั้นน้อยกว่าวันปัจจุบัน
            expired_products.append(product.id)  # เพิ่ม ID ของสินค้านั้นในลิสต์ expired_products

    return render(req, 'shop/show_product_search.html', {
        # ส่งข้อมูลไปยัง template 'shop/show_product_search.html'
        'show_product': show_product,  # ส่งข้อมูลสินค้าไปยัง template
        'category': categorys,  # ส่งข้อมูลหมวดหมู่สินค้าไปยัง template
        'provinces': Provinces.objects.all(),  # ดึงข้อมูลจังหวัดทั้งหมดและส่งไปยัง template
        'expired_products': expired_products  # ส่งข้อมูลสินค้าที่หมดอายุไปยัง template
    })



#หน้าคำแนะนำ
def advice_view(req):
    return render(req, 'shop/advice.html')


#แสดงอุปกรณ์ทั้งหมด
def product(request):
    category = Category.objects.all()  # ดึงข้อมูลหมวดหมู่สินค้าทั้งหมดจากฐานข้อมูล
    expired_products = []  # สร้างลิสต์ว่างเพื่อเก็บ ID ของสินค้าที่หมดอายุ

    if request.method == 'POST':
        # ถ้า request method เป็น POST
        search_query = request.POST.get('search_query')  # รับค่าคำค้นหาจากฟอร์ม
        allproduct = AllProduct.objects.filter(product_name__icontains=search_query)
        # ค้นหาสินค้าที่มีชื่อที่ตรงกับคำค้นหา (case-insensitive)
    else:
        # ถ้า request method ไม่ใช่ POST
        allproduct = AllProduct.objects.all()  # ดึงข้อมูลสินค้าทั้งหมดจากฐานข้อมูล

    for product in allproduct:
        # วนลูปเช็คสินค้าทุกตัวใน allproduct
        if product.lastdate and product.lastdate < timezone.now().date():
            # ถ้าสินค้ามีวันที่สิ้นสุดการเช่า (lastdate) และวันที่นั้นน้อยกว่าวันปัจจุบัน
            expired_products.append(product.id)  # เพิ่ม ID ของสินค้านั้นในลิสต์ expired_products

    context = {
        'allproduct': allproduct,  # ส่งข้อมูลสินค้าไปยัง context
        'category': category,  # ส่งข้อมูลหมวดหมู่สินค้าไปยัง context
        'provinces': Provinces.objects.all(),  # ดึงข้อมูลจังหวัดทั้งหมดและส่งไปยัง context
        'expired_products': expired_products  # ส่งข้อมูลสินค้าที่หมดอายุไปยัง context
    }
    return render(request, 'shop/show_product.html', context)  # ส่งข้อมูลไปยัง template 'shop/show_product.html'




#แสดงหมวดหมู่
def product_category(request, id):
    categorys = Category.objects.all()  # ดึงข้อมูลหมวดหมู่สินค้าทั้งหมดจากฐานข้อมูล
    expired_products = []  # สร้างลิสต์ว่างเพื่อเก็บ ID ของสินค้าที่หมดอายุ

    category = Category.objects.get(pk=id)  # ดึงข้อมูลหมวดหมู่สินค้าตาม ID ที่ระบุ

    if request.method == 'POST':
        # ถ้า request method เป็น POST
        search_query = request.POST.get('search_query')  # รับค่าคำค้นหาจากฟอร์ม
        allproduct = AllProduct.objects.filter(product_name__icontains=search_query)
        # ค้นหาสินค้าที่มีชื่อที่ตรงกับคำค้นหา (case-insensitive)
    else:
        # ถ้า request method ไม่ใช่ POST
        allproduct = AllProduct.objects.filter(category=category)  # ดึงข้อมูลสินค้าที่อยู่ในหมวดหมู่นั้น ๆ

    for product in allproduct:
        # วนลูปเช็คสินค้าทุกตัวใน allproduct
        if product.lastdate and product.lastdate < timezone.now().date():
            # ถ้าสินค้ามีวันที่สิ้นสุดการเช่า (lastdate) และวันที่นั้นน้อยกว่าวันปัจจุบัน
            expired_products.append(product.id)  # เพิ่ม ID ของสินค้านั้นในลิสต์ expired_products

    context = {
        'allproduct': allproduct,  # ส่งข้อมูลสินค้าไปยัง context
        'category': categorys,  # ส่งข้อมูลหมวดหมู่สินค้าไปยัง context
        'provinces': Provinces.objects.all(),  # ดึงข้อมูลจังหวัดทั้งหมดและส่งไปยัง context
        'expired_products': expired_products  # ส่งข้อมูลสินค้าที่หมดอายุไปยัง context
    }
    return render(request, 'shop/show_product_category.html', context)  # ส่งข้อมูลไปยัง template 'shop/show_product_category.html'


# โชว์รายละเอียด
@login_required
def Showdetall_product(req, product_id):
    # ดึงข้อมูลสินค้าจากฐานข้อมูลตาม product_id
    one_product = AllProduct.objects.get(pk=product_id)
    context = {'product': one_product}
    print(one_product.datetime)  # พิมพ์วันที่และเวลาของสินค้านั้นออกมาในคอนโซล
    # ส่งข้อมูลสินค้าไปยัง template 'shop/showdetall_product.html'
    return render(req, 'shop/showdetall_product.html', context)

# ลบของในตระกร้า
def delete(req, id):
    print(id)  # พิมพ์ ID ของ CartItem ที่จะถูกลบออกมาในคอนโซล
    CartItem.objects.get(pk=id).delete()  # ลบ CartItem ตาม ID ที่ระบุ
    # เปลี่ยนเส้นทางไปยังเส้นทางที่ชื่อ 'cart'
    return redirect('cart')

# ลบของในตระกร้าเมื่อเช่าในตระกร้า
def sell_buy_cart(req, id, cart):
    delete(req, cart)  # ลบรายการจากตระกร้า
    return add_sell_buy(req, id)  # ดำเนินการเช่าสินค้าต่อ

# เพิ่มของลงตระกร้า
def add_to_cart(req, product_id):
    product = get_object_or_404(AllProduct, pk=product_id)  # ดึงข้อมูลสินค้าจากฐานข้อมูลตาม product_id
    
    cart, created = Cart.objects.get_or_create(user=req.user)  # ดึงหรือสร้างตะกร้าสินค้าของผู้ใช้
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, user=req.user)  # ดึงหรือสร้าง CartItem ที่เชื่อมกับ cart และ product
    
    if not created:
        # ถ้า CartItem นี้มีอยู่แล้ว เพิ่มจำนวนสินค้าและคำนวณราคาสินค้าใหม่
        cart_item.quantity += 1
        cart_item.price = cart_item.quantity * product.product_price
        cart_item.save()
    else:
        # ถ้า CartItem นี้ถูกสร้างใหม่ กำหนดจำนวนสินค้าและราคาสินค้า
        cart_item.quantity = 1
        cart_item.price = product.product_price
        cart_item.save()
    
    return redirect('cart')  # เปลี่ยนเส้นทางไปยังเส้นทางที่ชื่อ 'cart'

# ตระกร้า
@login_required
def cart(req):
    Cart = CartItem.objects.filter(user=req.user)  # ดึงข้อมูล CartItem ทั้งหมดที่เชื่อมกับผู้ใช้
    context = {'Cart': Cart}  # สร้าง context ที่มีข้อมูล CartItem
    return render(req, 'shop/cart.html', context)  # ส่งข้อมูลไปยัง template 'shop/cart.html'

# การเช่าสำเร็จ
def add_sell_buy(req, id):
    product = AllProduct.objects.get(pk=id)  # ดึงข้อมูลสินค้าจากฐานข้อมูลตาม product_id
    data = Sell_Buy.objects.create(
        user=req.user,
        product=product,
        location=req.user.Profile.first().locations,
        phon=req.user.Profile.first().phon_numbers,
    )

    data.save()  # บันทึกข้อมูลการเช่าลงในฐานข้อมูล
    product.quantity -= 1  # ลดจำนวนสินค้าลง 1
    product.save()  # บันทึกการเปลี่ยนแปลงสินค้าลงในฐานข้อมูล
    context = {'product': product}  # สร้าง context ที่มีข้อมูลสินค้า
    return render(req, 'shop/Complete_buyproduct.html', context)  # ส่งข้อมูลไปยัง template 'shop/Complete_buyproduct.html'

# ค้นหาจังหวัด
def show_product_province(req, id):
    provinces = Provinces.objects.all()  # ดึงข้อมูลจังหวัดทั้งหมดจากฐานข้อมูล
    categorys = Category.objects.all()  # ดึงข้อมูลหมวดหมู่สินค้าทั้งหมดจากฐานข้อมูล
    province = get_object_or_404(Provinces, pk=id)  # ดึงข้อมูลจังหวัดตาม ID ที่ระบุ
    expired_products = []  # สร้างลิสต์ว่างเพื่อเก็บ ID ของสินค้าที่หมดอายุ

    if req.method == 'POST':
        search_query = req.POST.get('search')  # รับค่าคำค้นหาจากฟอร์ม
        # กรองข้อมูลตามคำค้นหาและจังหวัดที่เลือก
        allproduct = AllProduct.objects.filter(province=province, product_name__icontains=search_query)
    else:
        # ถ้าไม่มีการส่งคำค้นหามา
        allproduct = AllProduct.objects.filter(province=province)  # ดึงข้อมูลสินค้าที่อยู่ในจังหวัดนั้น ๆ

    for product in allproduct:
        # วนลูปเช็คสินค้าทุกตัวใน allproduct
        if product.lastdate and product.lastdate < timezone.now().date():
            # ถ้าสินค้ามีวันที่สิ้นสุดการเช่า (lastdate) และวันที่นั้นน้อยกว่าวันปัจจุบัน
            expired_products.append(product.id)  # เพิ่ม ID ของสินค้านั้นในลิสต์ expired_products

    context = {
        'allproduct': allproduct,  # ส่งข้อมูลสินค้าไปยัง context
        'category': categorys,  # ส่งข้อมูลหมวดหมู่สินค้าไปยัง context
        'provinces': provinces,  # ส่งข้อมูลจังหวัดไปยัง context
        'expired_products': expired_products,  # ส่งข้อมูลสินค้าที่หมดอายุไปยัง context
        'selected_province': province  # เพิ่มข้อมูลจังหวัดที่เลือกใน context
    }
    return render(req, 'shop/show_product_province.html', context)  # ส่งข้อมูลไปยัง template 'shop/show_product_province.html'

# ปล่อยเช่า
@login_required
def buy_product(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False).user = request.user  # กำหนดผู้ใช้ที่ปล่อยเช่า
            form.save()  # บันทึกข้อมูลการปล่อยเช่าลงในฐานข้อมูล
            return redirect('/shop/product/')  # เปลี่ยนเส้นทางไปยังหน้าสินค้าทั้งหมด
        else:
            form = UploadForm(request.POST, request.FILES)
    else:
        form = UploadForm()

    return render(request, 'shop/buy_product.html', {'form': form})  # ส่งฟอร์มไปยัง template 'shop/buy_product.html'

# แก้ไข
def edit_product(request, id):
    allproduct = AllProduct.objects.get(pk=id)  # ดึงข้อมูลสินค้าจากฐานข้อมูลตาม product_id
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=allproduct)
        if form.is_valid():
            form.save(commit=False).user = request.user  # กำหนดผู้ใช้ที่แก้ไขสินค้า
            form.save()  # บันทึกการแก้ไขสินค้าลงในฐานข้อมูล
            return redirect('/user/Edit_sell_product/')  # เปลี่ยนเส้นทางไปยังหน้าการแก้ไขสินค้าทั้งหมด
        else:
            form = EditForm(request.POST, request.FILES, instance=allproduct)
    else:
        form = EditForm(instance=allproduct)

    return render(request, 'shop/edit_product.html', {'form': form})  # ส่งฟอร์มไปยัง template 'shop/edit_product.html'
