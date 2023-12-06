from import_export import resources
from checkout.models import Order

class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('created_at','id','user__username', 'total','address__district')  