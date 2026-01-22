# apps/Sensors/forms.py
from django import forms
from .models import Sensor

class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = ['region', 'sensor_type', 'latitude', 'longitude', 'status']
        widgets = {
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Киев, Подол'}),
            'sensor_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'water_level'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_latitude', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_longitude', 'step': 'any'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }