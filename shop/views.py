from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,render,redirect,HttpResponseRedirect
from .models import * 
from .forms import *
from django.urls import reverse
from django.contrib import messages





def Location(req):
    return render(req, 'shop/location.html')

def searches(req):
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
    return render(req,'shop/show_product_search.html',{'show_product':show_product})

def advice_view(req):
    return render(req, 'shop/advice.html')


# def product(req):
#     allproduct = AllProduct.objects.all()
#     context = {'allproduct':allproduct}
#     return render(req, 'shop/show_product.html',context)

def product(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        # กรองข้อมูลตามคำค้นหา
        allproduct = AllProduct.objects.filter(product_name__icontains=search_query)
    else:
        # ถ้าไม่มีการส่งคำค้นหามา
        allproduct = AllProduct.objects.all()

    context = {'allproduct': allproduct}
    return render(request, 'shop/show_product.html', context)

@login_required
def Showdetall_product(req,product_id):
    one_product = AllProduct.objects.get(pk=product_id)
    context = {'product':one_product}
    print(one_product.datetime)
    return render(req, 'shop/showdetall_product.html',context)

def Buy_product(req):
    buy_ = Sell_Buy.objects.all()
    return render(req, 'shop/buy_product.html',{'sell_buy':buy_})

@login_required
def Sell_product(req):
    form = UploadForm()
    status = Status.objects.all()
    if req.method == 'POST':
        form = UploadForm(req.POST, req.FILES)
        if form.is_valid():
            form.save(commit=False).user = req.user
            form.save()
            return redirect('show_product')
    else:
        form = UploadForm()

    return render(req, 'shop/sell_product.html',{'form': form,'status':status})

# def Basket(req):
#     return render(req, 'shop/basket.html')

    
def update(req,id):
    form = Update()
    c = AllProduct.objects.get(pk=id)
    if req.method == 'POST':
        form = Update(req.POST,instance=c)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = Update(instance=c)

    return render(req,'shop/edit_product.html',{'form':form})

def delete(req, id):
    print(id)
    CartItem.objects.get(pk=id).delete()
    return redirect('cart')

def delete_datas(req, id):
    print(id)
    Sell_Buy.objects.get(pk=id).delete()
    return redirect('buy_product')

def add_to_cart(req, product_id):
    product = AllProduct.objects.get(pk=product_id)  # ดึงสินค้าจากฐานข้อมูลด้วย ID
    cart = Cart.objects.get(user=req.user.is_authenticated)
    
    cart_item = CartItem.objects.filter(cart=cart, product=product ,user=req.user)
    if cart_item:
        for i in cart_item:
            if i.product.id == product_id:
                i.quantity += 1 
                i.price = i.quantity * product.product_price
                i.save()
        
    else:
        cart_items = CartItem.objects.create(cart=cart, product=product ,user=req.user,price=product.product_price)
        cart_items.save()
    
   
    return redirect('cart')  # ส่งไปยังหน้าตะกร้าสินค้า

def cart(req):
    Cart = CartItem.objects.filter(user=req.user)
    context = {'Cart':Cart}
    return render(req,'shop/cart.html',context)

def add_sell_buy(req,id):
    product = AllProduct.objects.get(pk=id)
    data = Sell_Buy.objects.create(
        user = req.user,
        product = product,
    )
    data.save()
    product.quantity -= 1
    product.save()
    context = {
        'product':product,
    }
    return render(req, 'shop/Complete_buyproduct.html',context)

# def total_price(item_prices):
#     # คำนวณราคารวมโดยบวกราคาสินค้าทุกชิ้นในรายการ
#     total_price = sum(item_prices)
#     return total_price

# # ตัวอย่างการใช้งาน
# item_prices = []  # ราคาสินค้าแต่ละชิ้น
# total_price = total_price(item_prices)
# print("Total price:", total_price)



