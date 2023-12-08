from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(customuser)
admin.site.register(Size)
admin.site.register(category)
admin.site.register(brand)
admin.site.register(product)

