from django.db import models
from apps.Sensors.models import Sensor, SensorData

class AnalysisRule(models.Model):
    """
    Настройки пороговых значений.
    Соответствует 'rules: dict' из UML, но в виде удобной таблицы.
    """
    sensor_type = models.CharField(max_length=50, unique=True, help_text="Тип сенсора, к которому применяется правило")
    warning_threshold = models.FloatField(help_text="Значение, выше которого ставится Warning")
    critical_threshold = models.FloatField(help_text="Значение, выше которого ставится Critical")

    def __str__(self):
        return f"Rule for {self.sensor_type}: >{self.warning_threshold} (Warn), >{self.critical_threshold} (Crit)"


class Alert(models.Model):
    LEVEL_CHOICES = [
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ]

    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='alerts')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


    triggering_data = models.ForeignKey(SensorData, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def deactivate(self):
        """
        Метод из UML: deactivate()
        """
        self.is_active = False
        self.save()

    def __str__(self):
        status = "Active" if self.is_active else "Resolved"
        return f"[{self.level.upper()}] {self.sensor.region} ({status})"