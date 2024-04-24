from django.urls import path,include
from .views import *

urlpatterns = [
    path('',index, name="index"),
    path('predict_view/',predict_view, name="predict_view"),
    path('predict/', predict, name="predict"),
    path('show_data_save_predict/',show_data_save_predict, name="show_data_save_predict" ),
    path('delete_data/<int:id>/',delete_data, name="delete_data"),
]