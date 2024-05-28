from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,render,redirect,HttpResponseRedirect
from .models import * 
from .forms import *
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User

def searches(req):
   
    show_product = AllProduct.objects.all()
    categorys = Category.objects.all()
    # form = Search1()
    if req.method == 'POST':
        # form = Search1(req.POST)
        print(req.POST.get('time'))
        # if form.is_valid():
        time = req.POST.get('time')
        search = req.POST.get('search')
        print(search)
        if time is not None:
            show_product =  AllProduct.objects.filter(datetime__icontains=time) 
            for i in show_product:
                print(i)
        elif search is not None:
            show_product = AllProduct.objects.filter(product_name__icontains=search) or AllProduct.objects.filter(product_location__icontains=search) 
        else:
            show_product = AllProduct.objects.all()
    else:
        form = Search1()
        # show_product = []
    return render(req,'shop/show_product_search.html',{'show_product':show_product,'category':categorys,'provinces': Provinces.objects.all()})

def advice_view(req):
    return render(req, 'shop/advice.html')


# def product(req):
#     allproduct = AllProduct.objects.all()
#     context = {'allproduct':allproduct}
#     return render(req, 'shop/show_product.html',context)

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


@login_required
def Showdetall_product(req,product_id):
    one_product = AllProduct.objects.get(pk=product_id)
    context = {'product':one_product}
    print(one_product.datetime)
    return render(req, 'shop/showdetall_product.html',context)


@login_required
# def Sell_product(req):
#     categories = Category.objects.all()
#     provinces = Provinces.objects.all()
#     statuses = Status.objects.all()

#     if req.method == 'POST':
#         product_name = req.POST.get('product_name')
#         product_price = req.POST.get('product_price')
#         phon_number = req.POST.get('phon_number')
#         product_detail = req.POST.get('product_detail')
#         product_size = req.POST.get('product_size')
#         product_location = req.POST.get('product_location')
#         quantity = req.POST.get('quantity')
#         category_id = req.POST.get('category')
#         status_id = req.POST.get('status')
#         image = req.FILES.get('image')
#         province_id = req.POST.get('province_name')#เพิ่ม

#         category = Category.objects.get(id=category_id)
#         status = Status.objects.get(id=status_id)
#         province = Provinces.objects.get(id=province_id)#เพิ่ม

#         product = AllProduct(
#             user=req.user,
#             product_name=product_name,
#             product_price=product_price,
#             phon_number=phon_number,
#             product_detail=product_detail,
#             product_size=product_size,
#             product_location=product_location,
#             quantity=quantity,
#             category=category,
#             product_status=status,
#             province = province,#เพิ่ม
#             image=image,
#         )
#         product.save()
#         return redirect('show_product')

#     return render(req, 'shop/sell_product.html', {'category': categories, 'status': statuses,'provinces':provinces})


def delete(req, id):
    print(id)
    CartItem.objects.get(pk=id).delete()
    return redirect('cart')


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

def cart(req):
    
    Cart = CartItem.objects.filter(user=req.user)
    context = {'Cart':Cart}
    return render(req,'shop/cart.html',context)

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


def sell_buy_cart(req,id,cart):
    delete(req, cart)
    return add_sell_buy(req,id)

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



