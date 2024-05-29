from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,render,redirect,HttpResponseRedirect
from .models import * 
from .forms import *
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User


#ค้นหา

def searches(req):
    #ดึงออบเจ็กต์ทั้งหมดจากAllProductและCategoryมาไว้ในตัวแปล
    show_product = AllProduct.objects.all()
    categorys = Category.objects.all()
    
    if req.method == 'POST':
        search = req.POST.get('search')
        print(search)
        if search:
            show_product = AllProduct.objects.filter(product_name__icontains=search) or AllProduct.objects.filter(product_location__icontains=search)
        else:
            show_product = AllProduct.objects.all()
    else:
        form = Search1()

    return render(req, 'shop/show_product_search.html', {
        'show_product': show_product,
        'category': categorys,
        'provinces': Provinces.objects.all()
    })


#หน้าคำแนะนำ
def advice_view(req):
    return render(req, 'shop/advice.html')


#แสดงอุปกรณ์ทั้งหมด
def product(request):

    category = Category.objects.all()
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        # กรองข้อมูลตามคำค้นหา
        allproduct = AllProduct.objects.filter(product_name__icontains=search_query)
    else:
        # ถ้าไม่มีการส่งคำค้นหามา
        allproduct = AllProduct.objects.all()

    context = {'allproduct': allproduct,'category':category,'provinces': Provinces.objects.all()}
    return render(request, 'shop/show_product.html', context)

#แสดงหมวดหมู่
def product_category(request,id):
    categorys = Category.objects.all()
    
    category = Category.objects.get(pk=id)
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        # กรองข้อมูลตามคำค้นหา
        allproduct = AllProduct.objects.filter(product_name__icontains=search_query)
    else:
        # ถ้าไม่มีการส่งคำค้นหามา
        allproduct = AllProduct.objects.filter(category=category)

    context = {'allproduct': allproduct,'category':categorys,'provinces': Provinces.objects.all()}
    return render(request, 'shop/show_product_category.html', context)

#โชว์รายละเอียด
@login_required
def Showdetall_product(req,product_id):
    one_product = AllProduct.objects.get(pk=product_id)
    context = {'product':one_product}
    print(one_product.datetime)
    return render(req, 'shop/showdetall_product.html',context)


#ลบของในตระกร้า
def delete(req, id):
    print(id)
    CartItem.objects.get(pk=id).delete()
    return redirect('cart')

#ลบ
def sell_buy_cart(req,id,cart):
    delete(req, cart)
    return add_sell_buy(req,id)

#เพิ่มของลงตระกร้า
def add_to_cart(req, product_id):
    product = get_object_or_404(AllProduct, pk=product_id)
    
    # Retrieve or create the cart for the authenticated user
    cart, created = Cart.objects.get_or_create(user=req.user)
    
    # Check if the cart item already exists
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, user=req.user)
    
    if not created:
        # If it exists, update the quantity and price
        cart_item.quantity += 1
        cart_item.price = cart_item.quantity * product.product_price
        cart_item.save()
    else:
        # If it does not exist, set initial quantity and price
        cart_item.quantity = 1
        cart_item.price = product.product_price
        cart_item.save()
    
    return redirect('cart')

#ตระกร้า
@login_required
def cart(req):
    Cart = CartItem.objects.filter(user=req.user)
    context = {'Cart':Cart}
    return render(req,'shop/cart.html',context)

#สิ้นสุดการเช่า
def add_sell_buy(req,id):
    product = AllProduct.objects.get(pk=id)
    data = Sell_Buy.objects.create(
        user = req.user,
        product = product,
        location = req.user.Profile.first().locations,
        phon = req.user.Profile.first().phon_numbers,
    )

    data.save()
    product.quantity -= 1
    product.save()
    context = {
        'product':product,
    }
    return render(req, 'shop/Complete_buyproduct.html',context)




#ค้นหาจังหวัด
def show_product_province(req,id):
    provinces = Provinces.objects.all()
    categorys = Category.objects.all()
    province = Provinces.objects.get(pk=id)
    if req.method == 'POST':
        search_query = req.POST.get('search_query')
        # กรองข้อมูลตามคำค้นหา
        allproduct = AllProduct.objects.filter(product_name__icontains=search_query)
    else:
        # ถ้าไม่มีการส่งคำค้นหามา
        allproduct = AllProduct.objects.filter(province=province)

    context = {'allproduct': allproduct,'category':categorys,'provinces': Provinces.objects.all()}
    return render(req,'shop/show_product_province.html',context)
    

#ปล่อยเช่า
@login_required
def buy_product(request):
    if request.method == 'POST':
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save(commit=False).user = request.user
            form.save()
            return redirect('/shop/product/')
        else:
            form = UploadForm(request.POST,request.FILES)
    else:
        form = UploadForm()

    return render(request,'shop/buy_product.html',{'form':form})

#แก้ไข
def edit_product(request,id):
    allproduct = AllProduct.objects.get(pk=id)
    if request.method == 'POST':
        form = EditForm(request.POST,request.FILES,instance=allproduct)
        if form.is_valid():
            form.save(commit=False).user = request.user
            form.save()
            return redirect('/user/Edit_sell_product/')
        else:
            form = EditForm(request.POST,request.FILES,instance=allproduct)
    else:
        form = EditForm(instance=allproduct)

    return render(request,'shop/edit_product.html',{'form':form})



