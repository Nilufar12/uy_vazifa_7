from django import forms
from django.core.exceptions import ValidationError

from .models import Car, Brand


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        # fields = '__all__'
        fields = ['name', 'price', 'color', 'image', 'video', 'brand']
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

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError ('Narx 0dan katta bo\'lsin!!!')
        return price

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.islower():
            raise ValidationError('Car nomi kichik xarflarda bo\'lsin!!!')
        return name

    # def clean(self):
    #     cleaned_data = super().clean()
    #     price = cleaned_data.get('price')
    #     if price <= 0:
    #         raise ValidationError ('Narx 0dan katta bo\'lsin!!!')
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     name = cleaned_data.get('name')
    #     if not name.islower():
    #         raise ValidationError('Car nomi kichik xarflarda bo\'lsin!!!')


class CommentForm(forms.Form):
    text = forms.CharField(max_length=500)
