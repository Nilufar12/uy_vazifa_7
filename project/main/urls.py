from django.urls import path

from .views import home, brand_cars, car_detail, add_car, update_car, delete_car, create_comment, update_comment, \
    delete_comment

urlpatterns = [
    path('', home, name='home'),
    path('brand/<int:brand_id>/', brand_cars, name='brand_cars'),
    path('car/<int:car_id>/', car_detail, name='car_detail'),
    path('add/', add_car, name='add_car'),
    path('update/<int:pk>/', update_car, name='update'),
    path('delete/<int:pk>/', delete_car, name='delete'),
    path('cars/add/comment/<int:car_id>/', create_comment, name='create_comment'),
    path('cars/update/comment/<int:comment_id>/', update_comment, name='update_comment'),
    path('cars/delete/comment/<int:comment_id>/<int:car_id>/', delete_comment, name='delete_comment'),
]
