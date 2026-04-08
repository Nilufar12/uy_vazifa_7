from django.db import models


class Brand(models.Model):
    model = models.CharField(max_length=100)
    emblem = models.ImageField(upload_to='image/', null=True, blank=True)

    def __str__(self):
        return f'{self.model}'


class Car(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50)
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'
