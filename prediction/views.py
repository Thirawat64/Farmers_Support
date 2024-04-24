from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .models import *
import joblib

# Create your views here.

#สร้างโมเดล
models = joblib.load("C:\\Users\\THIRAWAT KAEWSANGA\\Downloads\\NewDecisionTree model.joblib")

def index(req):
    return render(req, 'prediction/index.html')
@login_required
def predict_view(req):
    return render(req, 'prediction/predict.html') 




def predict(request):
    if request.method == 'POST':
        ph_value = float(request.POST.get('ph_value'))
        max_temperature = float(request.POST.get('max_temperature'))
        humidity = float(request.POST.get('humidity'))
        precip = float(request.POST.get('precip'))
        soil_type = request.POST.get('soil_type')
        area_slope = float(request.POST.get('area_slope'))
        drainage = request.POST.get('drainage')


        soil_type_numeric = 0
        if soil_type == 'ดินเหนียว':
            soil_type_numeric = 0
        elif soil_type == 'ดินร่วน':
            soil_type_numeric = 1
        elif soil_type == 'ดินทราย':
            soil_type_numeric = 3

        drainage_numeric = 0
        if drainage == 'ไม่สามารถระบายน้ำได้':
            drainage_numeric = 0
        if drainage == 'ระบายน้ำได้':
            drainage_numeric = 1

        prediction = models.predict([[ph_value, max_temperature, humidity, precip, soil_type_numeric, area_slope, drainage_numeric]])
        if prediction == [0]:
            prediction = 'มันสำปะหลัง'
        if prediction == [1]:
            prediction = 'ข้าวโพด'
        if prediction == [2]:
            prediction = 'ปาล์มน้ำมัน'
        if prediction == [3]:
            prediction = 'ข้าว'
        if prediction == [4]:
            prediction = 'อ้อย'



        area_prediction = AreaPrediction.objects.create(
            user=request.user,
            ph_value=ph_value,
            max_temperature=max_temperature,
            humidity=humidity,
            precip=precip,
            soil_type=soil_type,
            area_slope=area_slope,
            drainage=drainage,
            predicted_plant=prediction

        )

        area_prediction.save()

    return render(request, 'prediction/result.html',{'prediction':prediction})


def show_data_save_predict(req):
    data_save_predict = AreaPrediction.objects.filter(user=req.user)
    return render(req, 'prediction/data_save_predict.html',{'data_save_predict':data_save_predict})

def delete_data(request, id):
    AreaPrediction.objects.get(pk=id).delete()
    return redirect('show_data_save_predict')