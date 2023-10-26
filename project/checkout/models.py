from django.db import models
from app.models import customuser
from phonenumber_field.modelfields import PhoneNumberField
from user.models import cart,cartitem


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


    

class payment_method(models.Model):
    choice=[('UPI','UPI'),
            ('COD','COD'),
            ]
    
    payment=models.CharField( max_length=10,choices=choice)

    def __str__(self):
        return self.payment
class address(models.Model):
    user=models.ForeignKey(customuser, on_delete=models.CASCADE)
    full_name=models.CharField( max_length=50)
    phone_number=PhoneNumberField()
    district=models.ForeignKey(district, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    pin=models.IntegerField()

    def __str__(self) -> str:
        return self.user.username
    
class order_status(models.Model):
    choice=[
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),

            ]
    status=models.CharField(choices=choice,max_length=20)

    def __str__(self) -> str:
        return self.status
    
class Order(models.Model):
    user = models.ForeignKey(customuser, on_delete=models.CASCADE)
    items = models.ManyToManyField(cartitem)
    address = models.ForeignKey(address,on_delete=models.CASCADE,null=True)
    payment=models.ForeignKey(payment_method, on_delete=models.SET_NULL,null=True)
    order_status=models.ForeignKey(order_status, on_delete=models.CASCADE,default=5)

    

    def __str__(self) -> str:
        return self.user.username
    

    