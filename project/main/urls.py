from django.urls import path

from .views import home, brand_cars, car_detail, add_car

urlpatterns = [
    path('', home, name='home'),
    path('brand/<int:brand_id>/', brand_cars, name='brand_cars'),
    path('car/<int:car_id>/', car_detail, name='car_detail'),
    path('add/', add_car, name='add_car')
]
