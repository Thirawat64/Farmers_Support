from django.contrib import admin
from .models import *
# Register your models here.
class AreaPredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ph_value', 'max_temperature', 'humidity', 'precip', 'soil_type', 'area_slope', 'drainage', 'predicted_plant')

# Register the model with the custom admin class
admin.site.register(AreaPrediction, AreaPredictionAdmin)