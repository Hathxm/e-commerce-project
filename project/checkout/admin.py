from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(address)
admin.site.register(district)
admin.site.register(Order)
# admin.site.register(payment_method)
# admin.site.register(order_status)
admin.site.register(wishlist)
admin.site.register(wallet)
admin.site.register(coupon)
admin.site.register(usercoupon)



