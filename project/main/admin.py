from django.contrib import admin

from .models import Car, Brand, Comment, CarMark, Dealer, Manufacturer

admin.site.site_header = 'Avtosalon'
# admin.site.login_template = 'admin/login.html'
# admin.site.logout_template = 'admin/logged_out.html'

admin.site.register(Brand)
admin.site.register(Car)
admin.site.register(Comment)
admin.site.register(CarMark)
admin.site.register(Dealer)
admin.site.register(Manufacturer)