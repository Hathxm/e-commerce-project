from django.contrib import admin
from . models import customuser,category,gender,brand,product,Size
# Register your models here.
admin.site.register(customuser)
admin.site.register(Size)
admin.site.register(category)
admin.site.register(gender)
admin.site.register(brand)
admin.site.register(product)

