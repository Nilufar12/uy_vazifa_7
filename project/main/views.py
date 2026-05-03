import paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .forms import CarForm, CommentForm
from .models import Brand, Car, Comment, CarMark


def home(request: HttpRequest):
    brands = Brand.objects.all()

    if request.user.is_authenticated:
        if request.GET.get('cars'):
            cars = []
            carmarks = CarMark.objects.filter(user=request.user)
            for carmark in carmarks:
                car = carmark.car
                car.like = True
                cars.append(car)
        else:
            cars = Car.objects.all()
            if request.user.is_authenticated:
                for car in cars:
                    res = car.carmarks.filter(user=request.user).exists()
                    if res:
                        car.like = True

    else:
        cars = Car.objects.all()

    paginator = Paginator(cars, 3)
    page = paginator.page(request.GET.get('page', 1))

    context = {
        'page': page,
        "brands": brands,
        'title': 'Avtosalon'
    }
    return render(request, 'main/home.html', context)


def brand_cars(request, brand_id):
    brand = Brand.objects.get(id=brand_id)
    cars = Car.objects.filter(brand_id=brand)
    if request.user.is_authenticated:
        for car in cars:
            res = car.carmarks.filter(user=request.user).exists()
            if res:
                car.like = True
    paginator = Paginator(cars, 3)
    page = paginator.get_page(request.GET.get('page', 1))

    context = {
        'page': page,
        'brand': brand,
        'cars': page,
        "brands": Brand.objects.all(),
        'title': brand.model
    }

    return render(request, 'main/detail.html', context)


def car_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    comments = Comment.objects.filter(car=car)
    if request.user.is_authenticated:
        if car.carmarks.filter(user=request.user).exists():
            car.like = True

    context = {
        "car": car,
        "brands": Brand.objects.all(),
        'title': car.name,
        'form': CommentForm(),
        'comments': comments
    }
    return render(request, 'main/car_detail.html', context)


def add_car(request: HttpRequest):
    if request.method == 'POST':
        form = CarForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            car = form.save()
            messages.success(request, "Mashina muvafaqqiyatli qo'shildi!!!")
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
        messages.success(request, "Mashina muvafaqqiyatli o\'chirildi")
        return redirect('home')
    context = {
        'car': car
    }
    messages.error(request, "Bu mashinani o'chirmoqchimisiz!!!")
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
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
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
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user or request.user.is_superuser:
        comment.delete()
    return redirect('car_detail', car_id=car_id)


@login_required(login_url='home')
def add_carmark(request, car_id: int):
    car = get_object_or_404(Car, pk=car_id)
    carmark, created = CarMark.objects.get_or_create(car=car, user=request.user)
    if not created:
        carmark.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url='home')
def carmark_cars(request):
    carmarks = CarMark.objects.filter(user=request.user)

    context = {
        'carmarks': carmarks
    }
    return render(request, 'main/home.html', context)
