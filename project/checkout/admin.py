from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(address)
admin.site.register(Order)
admin.site.register(wishlist)
admin.site.register(wallet)
admin.site.register(coupon)
admin.site.register(usercoupon)



