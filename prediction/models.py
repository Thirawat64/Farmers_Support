from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AreaPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ph_value = models.FloatField()
    max_temperature = models.FloatField()
    humidity = models.FloatField()
    precip = models.FloatField(max_length=100)
    soil_type = models.CharField(max_length=100)
    area_slope = models.FloatField(max_length=100)
    drainage = models.CharField(max_length=100)
    predicted_plant = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Prediction for {self.soil_type} soil"