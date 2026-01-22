from apps.Sensors.models import Sensor
from django.db import models

class MapSettings(models.Model):
    """
    Хранит настройки карты (API ключи, провайдер).
    Реализуем как Singleton (всегда одна запись).
    """
    MAP_PROVIDERS = [
        ('osm', 'OpenStreetMap'),
        ('google', 'Google Maps'),
        ('mapbox', 'Mapbox'),
    ]

    provider_name = models.CharField(max_length=50, choices=MAP_PROVIDERS, default='osm')
    api_key = models.CharField(max_length=255, blank=True, help_text="Leave empty for OpenStreetMap")


    default_lat = models.FloatField(default=50.45)
    default_lon = models.FloatField(default=30.52)
    default_zoom = models.IntegerField(default=10)

    class Meta:
        verbose_name = "Map Configuration"
        verbose_name_plural = "Map Configuration"

    def save(self, *args, **kwargs):

        if not self.pk and MapSettings.objects.exists():

            return MapSettings.objects.first()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Map Settings ({self.get_provider_name_display()})"