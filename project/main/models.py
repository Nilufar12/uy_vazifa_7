from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models


class Brand(models.Model):
    model = models.CharField(max_length=100)
    emblem = models.ImageField(upload_to='image/', null=True, blank=True)

    def __str__(self):
        return f'{self.model}'

    def __repr__(self):
        return f'{self.pk}: {self.model}'

    class Meta:
        verbose_name = 'Brandi'
        verbose_name_plural = 'Brandlar'


class Dealer(models.Model):

    MILD = [
        ('mild_a', 'Miloddan Avvalgi'),
        ('mild', 'Milodiy')
    ]

    full_name = models.CharField(max_length=255, verbose_name='To\'liq nomi')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='Manzil')
    joined_year = models.PositiveSmallIntegerField(verbose_name='Qo\'shilgan yili')
    mild = models.CharField(choices=MILD, default='mild')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Diller'
        verbose_name_plural = ' Dillerlar'


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nomi')
    address = models.CharField(max_length=150, verbose_name="Manzili")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ishlab chiqaruvchi'
        verbose_name_plural = "Ishlab chiqaruvchilar"


class Car(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nomi')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(0)], verbose_name='Narhi')
    color = models.CharField(max_length=50, verbose_name='Rangi')
    image = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name='Rasmi')
    video = models.FileField(upload_to='video/', null=True, blank=True,
                             validators=[FileExtensionValidator(['mp4', 'mov', 'avi'])], verbose_name='Videosi')
    dealer = models.ManyToManyField(Dealer, related_name='cars', verbose_name='Diller')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, verbose_name='Ishlab chiqaruvci')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Brandi')

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f"{self.pk} : {self.name}"

    class Meta:
        verbose_name = 'Mashina'
        verbose_name_plural = 'Mashinalar'
        ordering = ('pk',)


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

    def save(self,*args, **kwargs):
        if self.pk:
            old = Comment.objects.get(pk=self.pk)
            if old.text != self.text:
                self.edited =True
        super().save(*args, **kwargs)
    # def clean(self):
    #     if self.price is not None and self.price <= 0:
    #         raise ValidationError('Narh 0dan katta bo\'lsin!!!')

    class Meta:
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'


class CarMark(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='carmarks')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} -> {self.car.name}'

    class Meta:
        verbose_name = 'Tanlangan'
        verbose_name_plural = 'Tanlanganlar'
