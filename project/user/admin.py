from django.contrib import admin
from .models import cart,cartitem,item_status
# Register your models here.
admin.site.register(cart)
admin.site.register(cartitem)
admin.site.register(item_status)



