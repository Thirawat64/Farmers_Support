from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
import joblib
import os

# โหลดโมเดล
models = joblib.load('models/NewDecisionTree_model.joblib')

def index(req):
    return render(req, 'prediction/index.html')
 

@login_required
def predict_view(req):
    return render(req, 'prediction/predict.html') 



#ฟังชันทำนาย
def predict(request):
    if request.method == 'POST':
        name_area = request.POST.get('name_area')
        ph_value = float(request.POST.get('ph_value'))
        max_temperature = float(request.POST.get('max_temperature'))
        humidity = float(request.POST.get('humidity'))
        precip = float(request.POST.get('precip'))
        soil_type = request.POST.get('soil_type')
        area_slope = float(request.POST.get('area_slope'))
        drainage = request.POST.get('drainage')

        #สร้างเงื่อนไขเพื่อนเปลี่ยน soil_type เป็นตัวเลข
        soil_type_numeric = 0
        if soil_type == 'ดินเหนียว':
            soil_type_numeric = 0
        elif soil_type == 'ดินร่วน':
            soil_type_numeric = 1
        elif soil_type == 'ดินทราย':
            soil_type_numeric = 3

        #สร้างเงื่อนไขเพื่อนเปลี่ยน drainage เป็นตัวเลข
        drainage_numeric = 0
        if drainage == 'ไม่สามารถระบายน้ำได้':
            drainage_numeric = 0
        if drainage == 'ระบายน้ำได้':
            drainage_numeric = 1

        #นำข้อมูล มาทำนาย ด้วยโมเดล 
        prediction = models.predict([[ph_value, max_temperature, humidity, precip, soil_type_numeric, area_slope, drainage_numeric]])

        #สร้างเงื่อนไขเพื่อส่งออกเป็น output
        if 3.5 < ph_value < 9 and 10 < max_temperature < 45 and 19 < humidity < 101 and 499 < precip < 3001 and area_slope < 60:
            if prediction == [0]:
                prediction = 'มันสำปะหลัง'
            elif prediction == [1]:
                prediction = 'ข้าวโพด'
            elif prediction == [2]:
                prediction = 'ปาล์มน้ำมัน'
            elif prediction == [3]:
                prediction = 'ข้าว'
            elif prediction == [4]:
                prediction = 'อ้อย'
        else:
            prediction = 'พื้นที่ของคุณไม่เหมาะสมที่จะปลูกพืชในการวิเคราะห์ของเรา'

        #นำข้อมูลบันทึกลง database
        area_prediction = AreaPrediction.objects.create(
            user=request.user,
            ph_value=ph_value,
            name_area=name_area,
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

@login_required
def show_data_save_predict(req):
    data_save_predict = AreaPrediction.objects.filter(user=req.user).order_by('-user')
    return render(req, 'prediction/data_save_predict.html',{'data_save_predict':data_save_predict})

def delete_data(request, id):
    AreaPrediction.objects.get(pk=id).delete()
    return redirect('show_data_save_predict')