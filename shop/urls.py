from django.urls import path
from .views import *


urlpatterns = [
    path('',Location,name='location'),
    path('search/',searches,name='search'),
    path('advice/',advice_view,name='advice'),
    path('product/',product,name='show_product'),
    path('showdetall_product/<int:product_id>',Showdetall_product,name='Showdetall_product'),
    path('sell_product/',Sell_product,name='sell_product'),
    # path('buy_product/',Buy_product,name='buy_product'),
    path('add_to_cart/<int:product_id>/',add_to_cart, name='add_to_cart'),
    path('cart/',cart,name='cart'),
    path('delete/<int:id>/',delete, name="delete"),
    # path('delete_datas/<int:id>/',delete_datas, name="delete_datas"),
    path('add_sell_buy/<int:id>/',add_sell_buy, name="add_sell_buy"),
    path('product_category/<int:id>/',product_category, name="product_category"),
    path('sell_buy_cart/<int:id>/<int:cart>/',sell_buy_cart, name="sell_buy_cart"),
    

]

