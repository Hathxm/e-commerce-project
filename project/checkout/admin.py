from django.contrib import admin
from .models import address,district,Order,payment_method,order_status
# Register your models here.
admin.site.register(address)
admin.site.register(district)
admin.site.register(Order)
admin.site.register(payment_method)
admin.site.register(order_status)

