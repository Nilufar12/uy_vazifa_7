from django.core.exceptions import ValidationError
from django.db import models


class Brand(models.Model):
    model = models.CharField(max_length=100)
    emblem = models.ImageField(upload_to='image/', null=True, blank=True)

    def __str__(self):
        return f'{self.model}'

    def __repr__(self):
        return f'{self.pk}: {self.model}'


class Car(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50)
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return \
            f"{self.pk} : {self.name}"

    def clean(self):
        if self.price is not None and self.price <= 0:
            raise ValidationError('Narh 0dan katta bo\'lsin!!!')