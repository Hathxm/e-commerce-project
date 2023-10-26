from django.db import models
from app.models import product,customuser,Size

# Create your models here.

class item_status(models.Model):
     ORDER_STATUS_CHOICES = [
        ('Processing','Processing'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Return','Returned'),


    ]
     status=models.CharField(choices=ORDER_STATUS_CHOICES, max_length=10)
     
     def __str__(self) -> str:
        return self.status
    
class cartitem(models.Model): 
    product=models.ForeignKey(product, on_delete=models.CASCADE)
    size=models.ForeignKey(Size, on_delete=models.CASCADE,default=3)
    quantity=models.IntegerField(default=1)
    price=models.BigIntegerField(null=True)
    status=models.ForeignKey(item_status, on_delete=models.CASCADE, default=3)



    def __str__(self) -> str:
        return self.product.name

class cart(models.Model):
    user=models.OneToOneField(customuser, on_delete=models.CASCADE)
    items=models.ManyToManyField(cartitem)



    def __str__(self) -> str:
        return self.user.username    
    







 