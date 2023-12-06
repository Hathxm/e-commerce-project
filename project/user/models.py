from django.db import models
from app.models import product,customuser,Size

# Create your models here.

class item_status(models.Model):
     ORDER_STATUS_CHOICES = [
        ('Cancelled','Cancelled'),
        ('Return','Returned'),


    ]
     status=models.CharField(choices=ORDER_STATUS_CHOICES, max_length=10)
     
     def __str__(self) -> str:
        return self.status
    
class cartitem(models.Model): 
    user=models.ForeignKey(customuser, on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(product, on_delete=models.CASCADE)
    size=models.ForeignKey(Size, on_delete=models.CASCADE,default=1)
    quantity=models.IntegerField(default=1)
    price=models.BigIntegerField(null=True)
    is_deleted=models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.product.name
    
class ordereditems(models.Model):
    user=models.ForeignKey(customuser, on_delete=models.CASCADE)
    items=models.ManyToManyField(cartitem)
    total=models.BigIntegerField(null=True)
    coupon_applied=models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username
    
    










 