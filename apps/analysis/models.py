from django.db import models

# Create your models here.
from django.db import models
from apps.Sensors.models import Sensor

class Alert(models.Model):
    LEVEL_CHOICES = [
        ('warning', 'Увага'),
        ('critical', 'Небезпека'),
    ]

    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    message = models.TextField(default="Перевищено поріг")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"ALERT: {self.sensor.region} - {self.level}"