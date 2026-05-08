from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db import models
from django import forms

from .models import Car, Brand, Comment, CarMark, Dealer, Manufacturer

admin.site.site_header = 'Avtosalon'
# admin.site.login_template = 'admin/login.html'
# admin.site.logout_template = 'admin/logged_out.html'


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    exclude = ('user',)
    # readonly_fields = ('edited',)
    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(attrs={
                'rows': 3,
                'cols': 80,
            })
        }
    }


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',  'brand', 'color', 'manufacturer', 'get_image', 'get_video', 'make_discount')
    list_display_links = ('name',)
    list_filter = ('brand', 'manufacturer')
    list_editable = ('price', 'brand')
    search_fields = ('name', 'brand', 'color', 'manufacturer')
    inlines = [
        CommentInline
    ]

    # fields = (
    #     ('name', "brand"),
    #     ('price', 'color'),
    #     ('image', 'video')
    # )
    fieldsets = [
        (
            'Asosiy',
            {
                'fields': ['name', 'brand']
            },
        ),
        (
            "Narhlar",
            {
                'fields': ['price']
            }
        ),
        (
            "Medialar",
            {
                'fields': ['image', 'video']
            }
        ),
    ]

    @admin.display(description='Rasmi')
    def get_image(self, car):
        if car.image:
            return mark_safe(f'<img src="{car.image.url}" width="100px">')
        else:
            return "_"

    @admin.display(description='Videosi')
    def get_video(self, car):
        if car.video:
            return mark_safe(f'<video src="{car.video.url}"')
        else:
            return '_'

    @admin.display(description='10% chegirma')
    def make_discount(self, car):
        return car.price - (car.price * 10 / 100)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(CarMark)
class CarMarkAdmin(admin.ModelAdmin):
    pass


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    pass


@admin.register(Manufacturer)
class Manufacturer(admin.ModelAdmin):
    pass
