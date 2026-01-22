from django import forms
from .models import Subscriber

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['region', 'email', 'phone']
        widgets = {
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Напишіть з якого ви міста для отримання сповіщення про тривогу'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+380...'}),
        }