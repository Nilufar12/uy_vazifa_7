from django.http import HttpRequest
from django.shortcuts import render

from .models import Brand, Car


def home(request: HttpRequest):
    brands = Brand.objects.all()
    cars = Car.objects.all()

    context = {
        "brands": brands,
        'cars': cars,
        "brands": Brand.objects.all()
    }
    return render(request, 'main/home.html', context)


def brand_cars(request, brand_id):
    brand = Brand.objects.get(id=brand_id)
    cars = Car.objects.filter(brand_id=brand)

    context = {
        'brand': brand,
        'cars': cars,
        "brands": Brand.objects.all()
    }

    return render(request, 'main/home.html', context)


def car_detail(request, car_id):
    car = Car.objects.get(id=car_id)

    context = {
        "car": car,
        "brands": Brand.objects.all()
    }
    return render(request, 'main/home.html', context)