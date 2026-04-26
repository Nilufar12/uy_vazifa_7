from django.http import HttpRequest
from django.shortcuts import render, redirect

from .forms import CarForm, CommentForm
from .models import Brand, Car


def home(request: HttpRequest):
    brands = Brand.objects.all()
    cars = Car.objects.all()

    context = {
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
        "brands": Brand.objects.all(),
        'title': brand.model
    }

    return render(request, 'main/detail.html', context)


def car_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    context = {
        "car": car,
        "brands": Brand.objects.all(),
        'title': car.name,
        'form': CommentForm()
    }
    return render(request, 'main/detail.html', context)


def add_car(request: HttpRequest):
    if request.method == 'POST':
        form = CarForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            car = form.save()
            return redirect('car_detail', car_id=car.id)
    else:
        form = CarForm()
    context = {'form': form}
    return render(request, 'main/add_car.html', context)


def update_car(request, pk: int):
    car = Car.objects.get(pk=pk)
    if request.method == "POST":
        form = CarForm(data=request.POST, files=request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_detail', car_id=car.id)
<<<<<<< HEAD
    else:
=======
    else: 
>>>>>>> 8981af38019b4f4c740adc9fb5fd68fdb80d58e8
        form = CarForm(instance=car)

    return render(request, 'main/update_car.html', {'form': form})


def delete_car(request, pk):
    car = Car.objects.get(pk=pk)
    if request.method == 'POST':
        car.delete()
        return redirect('home')
    context = {
        'car': car
    }
<<<<<<< HEAD
    return render(request, 'main/delete.html', context)


def create_comment(request):
    pass
=======
    return render(request, 'main/delete.html', context)
>>>>>>> 8981af38019b4f4c740adc9fb5fd68fdb80d58e8
