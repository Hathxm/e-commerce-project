from django.db import models
from app.models import customuser
from phonenumber_field.modelfields import PhoneNumberField
from user.models import cartitem,product,ordereditems
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date


# Create your models here.


class district(models.Model):
    choice_fields=[('Kasaragod','Kasaragod'),
                   ('Kannur','Kannur'),
                   ('Kozhikode','Kozhikode'),
                   ('Malappuram','Malappuram'),
                   ('Thrissur','Thrissur'),
                   ('Ernankulam','Kochi'),
                   ('Alapuzha','Alapuzha'),
                   ('Kottayam','Kottayam'),
                   ('Kollam','Kollam'),
                   ('Palakkad','Palakkad'),
                   ('Trivandrum','Trivandrum')
                   ]
    district=models.CharField( max_length=20,choices=choice_fields)
 

    def __str__(self) -> str:
        return self.district


    

class address(models.Model):
    user=models.ForeignKey(customuser, on_delete=models.CASCADE) 
    full_name=models.CharField( max_length=50)
    phone_number=PhoneNumberField()
    district=models.ForeignKey(district, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    pin=models.IntegerField()

    def __str__(self) -> str:
        return self.user.username
    

    
class coupon(models.Model):
    name=models.CharField(max_length=7)
    discount_percentage = models.IntegerField()
    valid_from=models.DateTimeField( auto_now=False, auto_now_add=False)
    valid_to=models.DateTimeField( auto_now=False, auto_now_add=False)
    is_deleted=models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.name
    
class usercoupon(models.Model):
    user=models.ForeignKey(customuser, on_delete=models.CASCADE)
    coupon=models.ForeignKey(coupon, on_delete=models.CASCADE)
    used_at=models.DateTimeField(auto_now=False, auto_now_add=False)
    

    
class Order(models.Model):
    user = models.ForeignKey(customuser, on_delete=models.CASCADE)
    items=models.ForeignKey(ordereditems, on_delete=models.CASCADE)
    address=models.ForeignKey(address,on_delete=models.CASCADE,null=True)
    payment=models.CharField(max_length=50)
    order_status=models.CharField(max_length=50)
    total=models.BigIntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    coupon=models.ForeignKey(coupon,on_delete=models.CASCADE,null=True,default=None,blank=True)


    def __str__(self) -> str:
        return self.user.username
    
class wishlist(models.Model):
    user=models.ForeignKey(customuser, on_delete=models.CASCADE)
    items=models.ManyToManyField(product)

    def __str__(self) -> str:
        return self.user.username
    
class wallet(models.Model):
    user=models.OneToOneField(customuser,on_delete=models.CASCADE)
    money=models.BigIntegerField(default=0)

    def __str__(self) -> str:
        return self.user.username


    

    

    




    