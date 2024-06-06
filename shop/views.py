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
    #ดึงออบเจ็กต์ทั้งหมดจากAllProductและCategoryมาไว้ในตัวแปล
    show_product = AllProduct.objects.all()
    categorys = Category.objects.all()
    #สร้างลิสต์เปล่าชื่อ expired_products เพื่อใช้เก็บ ID ของสินค้าที่หมดอายุ
    expired_products = []
    
    #เช็คว่าคำขอเป็นแบบ POST หรือไม่
    if req.method == 'POST':
        #ดึงค่าจากฟอร์มที่ชื่อ search มาเก็บในตัวแปร search
        search = req.POST.get('search')
        print(search)

        #เช็คว่ามีค่าของ search หรือไม่
        if search:
            #ถ้ามีค่า search จะทำการค้นหาสินค้าในโมเดล AllProduct โดยเช็คจาก product_name หรือ product_location ที่มีค่านั้นอยู่ และเก็บผลลัพธ์ไว้ใน show_product
            show_product = AllProduct.objects.filter(product_name__icontains=search) or AllProduct.objects.filter(product_location__icontains=search)
        else:
            #ดึงข้อมูลทั้งหมดจาก AllProduct มาเก็บไว้ใน show_product
            show_product = AllProduct.objects.all()
    #ถ้าคำขอไม่ใช่แบบ POST
    else:
        #สร้างฟอร์มชื่อ Search1
        form = Search1()
    #วนลูปผ่านแต่ละสินค้าใน show_product
    for product in show_product:
        #เช็คว่ามีค่า lastdate ของสินค้าและวันหมดอายุน้อยกว่าวันปัจจุบันหรือไม่
        if product.lastdate and product.lastdate < timezone.now().date():
            #ถ้าสินค้าหมดอายุ จะเพิ่ม ID ของสินค้านั้นลงใน expired_products
            expired_products.append(product.id)
    #ส่งผลลัพธ์ไปยังเทมเพลต show_product_search.html
    return render(req, 'shop/show_product_search.html', {
        #ส่งตัวแปร show_product ไปยังเทมเพลต
        'show_product': show_product,
        #ส่งตัวแปร categorys ไปยังเทมเพลต
        'category': categorys,
        #ส่งข้อมูลของ Provinces ทั้งหมดไปยังเทมเพลต
        'provinces': Provinces.objects.all(),
        #ส่งลิสต์ expired_products ไปยังเทมเพลต
        'expired_products': expired_products
    })


#หน้าคำแนะนำ
def advice_view(req):
    return render(req, 'shop/advice.html')


#แสดงอุปกรณ์ทั้งหมด
def product(request):
    # ดึงข้อมูลทั้งหมดจากโมเดล Category มาเก็บไว้ในตัวแปร category
    category = Category.objects.all()
    # สร้างลิสต์เปล่าชื่อ expired_products เพื่อใช้เก็บ ID ของสินค้าที่หมดอายุ
    expired_products = []

    if request.method == 'POST':
        # ดึงค่าจากฟอร์มที่ชื่อ search_query มาเก็บในตัวแปร search_query
        search_query = request.POST.get('search_query')
        # ค้นหาสินค้าในโมเดล AllProduct โดยเช็คจาก product_name ที่มีค่านั้นอยู่
        allproduct = AllProduct.objects.filter(product_name__icontains=search_query)
    else:
        # ถ้าคำขอไม่ใช่แบบ POST ดึงข้อมูลทั้งหมดจาก AllProduct มาเก็บไว้ใน allproduct
        allproduct = AllProduct.objects.all()

    # วนลูปผ่านแต่ละสินค้าใน allproduct
    for product in allproduct:
        # เช็คว่ามีค่า lastdate ของสินค้าและวันหมดอายุน้อยกว่าวันปัจจุบันหรือไม่
        if product.lastdate and product.lastdate < timezone.now().date():
            # ถ้าสินค้าหมดอายุ จะเพิ่ม ID ของสินค้านั้นลงใน expired_products
            expired_products.append(product.id)

    # สร้าง context เพื่อส่งตัวแปรไปยังเทมเพลต
    context = {
        'allproduct': allproduct,  # ส่งตัวแปร allproduct ไปยังเทมเพลต
        'category': category,      # ส่งตัวแปร category ไปยังเทมเพลต
        'provinces': Provinces.objects.all(),  # ส่งข้อมูลของ Provinces ทั้งหมดไปยังเทมเพลต
        'expired_products': expired_products  # ส่งลิสต์ expired_products ไปยังเทมเพลต
    }
    # ส่งผลลัพธ์ไปยังเทมเพลต show_product.html
    return render(request, 'shop/show_product.html', context)



#แสดงหมวดหมู่
def product_category(request, id):
    # ดึงข้อมูลทั้งหมดจากโมเดล Category มาเก็บไว้ในตัวแปร categorys
    categorys = Category.objects.all()
    # สร้างลิสต์เปล่าชื่อ expired_products เพื่อใช้เก็บ ID ของสินค้าที่หมดอายุ
    expired_products = []

    # ดึงข้อมูลของ Category ที่มี primary key เท่ากับ id มาเก็บในตัวแปร category
    category = Category.objects.get(pk=id)
    
    if request.method == 'POST':
        # ดึงค่าจากฟอร์มที่ชื่อ search_query มาเก็บในตัวแปร search_query
        search_query = request.POST.get('search_query')
        # กรองข้อมูลตามคำค้นหาในโมเดล AllProduct โดยเช็คจาก product_name ที่มีค่านั้นอยู่
        allproduct = AllProduct.objects.filter(product_name__icontains=search_query)
    else:
        # ถ้าไม่มีการส่งคำค้นหามา กรองข้อมูลจาก AllProduct ตามหมวดหมู่ category
        allproduct = AllProduct.objects.filter(category=category)

    # วนลูปผ่านแต่ละสินค้าใน allproduct
    for product in allproduct:
        # เช็คว่ามีค่า lastdate ของสินค้าและวันหมดอายุน้อยกว่าวันปัจจุบันหรือไม่
        if product.lastdate and product.lastdate < timezone.now().date():
            # ถ้าสินค้าหมดอายุ จะเพิ่ม ID ของสินค้านั้นลงใน expired_products
            expired_products.append(product.id)

    # สร้าง context เพื่อส่งตัวแปรไปยังเทมเพลต
    context = {
        'allproduct': allproduct,  # ส่งตัวแปร allproduct ไปยังเทมเพลต
        'category': categorys,     # ส่งตัวแปร categorys ไปยังเทมเพลต
        'provinces': Provinces.objects.all(),  # ส่งข้อมูลของ Provinces ทั้งหมดไปยังเทมเพลต
        'expired_products': expired_products   # ส่งลิสต์ expired_products ไปยังเทมเพลต
    }
    # ส่งผลลัพธ์ไปยังเทมเพลต show_product_category.html
    return render(request, 'shop/show_product_category.html', context)


#โชว์รายละเอียด
@login_required
def Showdetall_product(req, product_id):
    # ดึงข้อมูลของสินค้าที่มี primary key เท่ากับ product_id มาเก็บในตัวแปร one_product
    one_product = AllProduct.objects.get(pk=product_id)
    
    # สร้าง context เพื่อส่งตัวแปรไปยังเทมเพลต
    context = {'product': one_product}
    
    # พิมพ์ค่า datetime ของสินค้า (สำหรับการดีบัก)
    print(one_product.datetime)
    
    # ส่งผลลัพธ์ไปยังเทมเพลต showdetall_product.html
    return render(req, 'shop/showdetall_product.html', context)


# ฟังก์ชันลบ
def delete(req, id):
    # พิมพ์ค่า id ออกมา (สำหรับการดีบัก)
    print(id)
    
    # ดึงข้อมูลของ CartItem ที่มี primary key เท่ากับ id และลบออบเจ็กต์นั้นออกจากฐานข้อมูล
    CartItem.objects.get(pk=id).delete()
    
    # เปลี่ยนเส้นทางไปยังเส้นทางที่ชื่อ 'cart'
    return redirect('cart')

# ฟังก์ชันขาย-ซื้อจากตะกร้า
def sell_buy_cart(req, id, cart):
    # เรียกใช้ฟังก์ชัน delete เพื่อลบสินค้าที่อยู่ในตะกร้า
    delete(req, cart)
    
    # เรียกใช้ฟังก์ชัน add_sell_buy เพื่อลงบันทึกการขาย-ซื้อสินค้า
    return add_sell_buy(req, id)


# เพิ่มของลงตะกร้า
def add_to_cart(req, product_id):
    # ดึงข้อมูลของสินค้าที่มี primary key เท่ากับ product_id ถ้าไม่เจอจะคืนค่า 404
    product = get_object_or_404(AllProduct, pk=product_id)
    
    # ดึงข้อมูลของตะกร้าสินค้าที่ผู้ใช้สร้างไว้ ถ้าไม่มีจะสร้างใหม่
    cart, created = Cart.objects.get_or_create(user=req.user)
    
    # ดึงข้อมูลของ CartItem ที่ตรงกับ cart และ product ถ้าไม่มีจะสร้างใหม่
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, user=req.user)
    
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
    
    # เปลี่ยนเส้นทางไปยังเส้นทางที่ชื่อ 'cart'
    return redirect('cart')


#ตระกร้า
@login_required
def cart(req):
    # ดึงข้อมูลของ CartItem ทั้งหมดที่ตรงกับผู้ใช้ปัจจุบัน
    Cart = CartItem.objects.filter(user=req.user)
    
    # สร้าง context เพื่อส่งตัวแปรไปยังเทมเพลต
    context = {'Cart': Cart}
    
    # ส่งผลลัพธ์ไปยังเทมเพลต cart.html
    return render(req, 'shop/cart.html', context)


# สิ้นสุดการเช่า
def add_sell_buy(req, id):
    # ดึงข้อมูลของสินค้าที่มี primary key เท่ากับ id มาเก็บในตัวแปร product
    product = AllProduct.objects.get(pk=id)
    
    # สร้างออบเจ็กต์ Sell_Buy โดยกำหนดค่าจากข้อมูลที่รับเข้ามา
    data = Sell_Buy.objects.create(
        user=req.user,  # กำหนดผู้ใช้ที่ทำการซื้อขาย
        product=product,  # กำหนดสินค้าที่ทำการซื้อขาย
        location=req.user.Profile.first().locations,  # ดึงข้อมูลสถานที่จากโปรไฟล์ของผู้ใช้
        phon=req.user.Profile.first().phon_numbers,  # ดึงข้อมูลเบอร์โทรศัพท์จากโปรไฟล์ของผู้ใช้
    )

    # บันทึกข้อมูลการซื้อขาย
    data.save()
    
    # ลดจำนวนสินค้าลง 1 หน่วย
    product.quantity -= 1
    product.save()
    
    # สร้าง context เพื่อส่งตัวแปรไปยังเทมเพลต
    context = {
        'product': product,
    }
    
    # ส่งผลลัพธ์ไปยังเทมเพลต Complete_buyproduct.html พร้อมกับ context ที่สร้างขึ้น
    return render(req, 'shop/Complete_buyproduct.html', context)



#ค้นหาจังหวัด
def show_product_province(req, id):
    # ดึงข้อมูลทั้งหมดจากโมเดล Provinces มาเก็บไว้ในตัวแปร provinces
    provinces = Provinces.objects.all()
    
    # ดึงข้อมูลทั้งหมดจากโมเดล Category มาเก็บไว้ในตัวแปร categorys
    categorys = Category.objects.all()
    
    # ดึงข้อมูลของจังหวัดที่มี primary key เท่ากับ id มาเก็บในตัวแปร province
    province = Provinces.objects.get(pk=id)
    
    # สร้างลิสต์เปล่าชื่อ expired_products เพื่อใช้เก็บ ID ของสินค้าที่หมดอายุ
    expired_products = []

    if req.method == 'POST':
        # ดึงค่าจากฟอร์มที่ชื่อ search_query มาเก็บในตัวแปร search_query
        search_query = req.POST.get('search_query')
        
        # กรองข้อมูลตามคำค้นหาในโมเดล AllProduct โดยเช็คจาก product_name ที่มีค่านั้นอยู่
        allproduct = AllProduct.objects.filter(product_name__icontains=search_query)
    else:
        # ถ้าไม่มีการส่งคำค้นหามา กรองข้อมูลจาก AllProduct ตามจังหวัด province
        allproduct = AllProduct.objects.filter(province=province)

    # วนลูปผ่านแต่ละสินค้าใน allproduct
    for product in allproduct:
        # เช็คว่ามีค่า lastdate ของสินค้าและวันหมดอายุน้อยกว่าวันปัจจุบันหรือไม่
        if product.lastdate and product.lastdate < timezone.now().date():
            # ถ้าสินค้าหมดอายุ จะเพิ่ม ID ของสินค้านั้นลงใน expired_products
            expired_products.append(product.id)

    # สร้าง context เพื่อส่งตัวแปรไปยังเทมเพลต
    context = {
        'allproduct': allproduct,  # ส่งตัวแปร allproduct ไปยังเทมเพลต
        'category': categorys,     # ส่งตัวแปร categorys ไปยังเทมเพลต
        'provinces': provinces,    # ส่งตัวแปร provinces ไปยังเทมเพลต
        'expired_products': expired_products  # ส่งลิสต์ expired_products ไปยังเทมเพลต
    }
    
    # ส่งผลลัพธ์ไปยังเทมเพลต show_product_province.html
    return render(req, 'shop/show_product_province.html', context)

    

# ฟังก์ชันปล่อยเช่า
@login_required
def buy_product(request):
    # เช็คว่าถ้า request เป็นแบบ POST
    if request.method == 'POST':
        # สร้างฟอร์ม UploadForm โดยรับข้อมูลจาก request.POST และ request.FILES
        form = UploadForm(request.POST, request.FILES)
        
        # เช็คว่าฟอร์ม valid หรือไม่
        if form.is_valid():
            # กำหนดผู้ใช้ปัจจุบันให้กับฟอร์ม
            form.save(commit=False).user = request.user
            # บันทึกฟอร์ม
            form.save()
            # เปลี่ยนเส้นทางไปยัง /shop/product/
            return redirect('/shop/product/')
        else:
            # ถ้าฟอร์มไม่ valid สร้างฟอร์มใหม่โดยรับข้อมูลจาก request.POST และ request.FILES
            form = UploadForm(request.POST, request.FILES)
    else:
        # ถ้า request ไม่ใช่แบบ POST สร้างฟอร์มเปล่า
        form = UploadForm()

    # ส่งฟอร์มไปยังเทมเพลต buy_product.html
    return render(request, 'shop/buy_product.html', {'form': form})


# ฟังก์ชันแก้ไขสินค้า
def edit_product(request, id):
    # ดึงข้อมูลของสินค้าที่มี primary key เท่ากับ id มาเก็บในตัวแปร allproduct
    allproduct = AllProduct.objects.get(pk=id)
    
    # เช็คว่าถ้า request เป็นแบบ POST
    if request.method == 'POST':
        # สร้างฟอร์ม EditForm โดยรับข้อมูลจาก request.POST, request.FILES และ instance ของ allproduct
        form = EditForm(request.POST, request.FILES, instance=allproduct)
        
        # เช็คว่าฟอร์ม valid หรือไม่
        if form.is_valid():
            # กำหนดผู้ใช้ปัจจุบันให้กับฟอร์ม
            form.save(commit=False).user = request.user
            # บันทึกฟอร์ม
            form.save()
            # เปลี่ยนเส้นทางไปยัง /user/Edit_sell_product/
            return redirect('/user/Edit_sell_product/')
        else:
            # ถ้าฟอร์มไม่ valid สร้างฟอร์มใหม่โดยรับข้อมูลจาก request.POST, request.FILES และ instance ของ allproduct
            form = EditForm(request.POST, request.FILES, instance=allproduct)
    else:
        # ถ้า request ไม่ใช่แบบ POST สร้างฟอร์มโดยมี instance ของ allproduct
        form = EditForm(instance=allproduct)

    # ส่งฟอร์มไปยังเทมเพลต edit_product.html
    return render(request, 'shop/edit_product.html', {'form': form})
