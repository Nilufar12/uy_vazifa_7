from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
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
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(0)])
    color = models.CharField(max_length=50)
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    video = models.FileField(upload_to='video/', null=True, blank=True,
                             validators=[FileExtensionValidator(['mp4', 'mov', 'avi'])])
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f"{self.pk} : {self.name}"

    # def clean(self):
    #     if self.price is not None and self.price <= 0:
    #         raise ValidationError('Narh 0dan katta bo\'lsin!!!')


class Comment(models.Model):
    text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return f"{self.pk} : {self.text}"