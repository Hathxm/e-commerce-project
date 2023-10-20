from django.db import models
from app.models import product,customuser,Size
# Create your models here.
    
class cartitem(models.Model):
    product=models.ForeignKey(product, on_delete=models.CASCADE)
    size=models.ForeignKey(Size, on_delete=models.CASCADE,default=2)
    quantity=models.IntegerField(default=1)
    price=models.BigIntegerField(null=True)


    def __str__(self) -> str:
        return self.product.name

class cart(models.Model):
    user=models.OneToOneField(customuser, on_delete=models.CASCADE)
    items=models.ManyToManyField(cartitem)
    



    def __str__(self) -> str:
        return self.user.username    

 