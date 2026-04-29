from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.template.context_processors import request

from .forms import CarForm, CommentForm
from .models import Brand, Car, Comment


def home(request: HttpRequest):
    brands = Brand.objects.all()
    cars = Car.objects.all()

    context = {
        'cars': cars,
        "brands": brands
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
    comments = Comment.objects.filter(car=car)
    context = {
        "car": car,
        "brands": Brand.objects.all(),
        'title': car.name,
        'form': CommentForm(),
        'comments': comments
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
    else:
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
    return render(request, 'main/delete.html', context)


def create_comment(request, car_id: int):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(data=request.POST)
            if form.is_valid():
                car = Car.objects.get(pk=car_id)
                comment = form.save(commit=False)
                comment.car = car
                comment.user = request.user
                comment.save()
        return redirect('car_detail', car_id)
    else:
        return redirect('home')


def update_comment(request: HttpRequest, comment_id: int):
    comment = Comment.objects.get(pk=comment_id)
    if request.method == 'POST':
        form = CommentForm(data=request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.edited = True
            comment.save()
            return redirect('car_detail', car_id=comment.car.id)

    else:
        form = CommentForm(instance=comment)
        context = {
            'form': form
        }
    return render(request, 'main/update_comment.html', context)


@login_required(login_url='home')
def delete_comment(request: HttpRequest, comment_id: int, car_id: int):
    comment = Comment.objects.get(pk=comment_id)
    if comment.user == request.user or request.user.is_superuser:
        comment.delete()
    return redirect('car_detail', car_id=comment.car.id)



