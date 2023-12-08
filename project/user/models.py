from django.db import models
from app.models import product,customuser,Size

# Create your models here.

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
    
class tocontact(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField( max_length=254)
    message=models.TextField()

    def __str__(self) -> str:
        return self.first_name 
    



    
    










 