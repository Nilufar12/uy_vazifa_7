from django import forms

from .models import Car, Brand


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        # fields = '__all__'
        fields = ['name', 'price', 'color', 'image', 'brand']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'price': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 1
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'brand': forms.Select(attrs={
                'class': 'form-select'
            })
        }









