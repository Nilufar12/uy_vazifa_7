from django import forms

from .models import Car, Brand


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
