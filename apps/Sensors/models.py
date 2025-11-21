from django.db import models


class Sensor(models.Model):
    REGION_CHOICES = [
        ('yaremche', 'Яремчанський'),
        ('verkhovyna', 'Верховинський'),
        ('kosiv', 'Косівський'),
    ]
    TYPE_CHOICES = [
        ('water_level', 'Рівень води'),
        ('precipitation', 'Опади'),
    ]

    sensor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Назва")
    region = models.CharField(max_length=50, choices=REGION_CHOICES)
    sensor_type = models.CharField(max_length=50, choices=TYPE_CHOICES, name='type')
    status = models.CharField(max_length=20, default='online')

    # Координати для MapService
    latitude = models.FloatField(default=48.45)
    longitude = models.FloatField(default=24.55)

    def __str__(self):
        return f"{self.name} ({self.region})"

class SensorData(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='data')
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor.name}: {self.value} at {self.timestamp}"