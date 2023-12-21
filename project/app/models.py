from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from image_cropping import ImageRatioField
from django.utils import timezone

# Create your models here.
class customuser(AbstractUser):
    user_img=models.ImageField( upload_to='user_pics', height_field=None, width_field=None, max_length=None,null=True)
    is_deleted=models.BooleanField(default=False)
    otp=models.IntegerField(null=True,blank=True)
    otp_created_at=models.DateTimeField(null=True, blank=True)
    phone_number=PhoneNumberField(null=True)

    
class Size(models.Model):
    sizze = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]
    size=models.CharField(max_length=50,choices=sizze)
    price_increment=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.size
    

class category(models.Model):
    choice=[
        ('Tops','Top wear'),
        ('Lowers','Lower wear'),
        ('Accessories','Accessories'),

        ]
    wear=models.CharField( max_length=50,choices=choice)
    is_deleted=models.BooleanField(default=False)
    discount_percentage=models.FloatField(default=0)
    valid_to=models.DateTimeField(null=True)


    def __str__(self) -> str:
        return self.wear

     
class brand(models.Model):
    name=models.CharField( max_length=50)
    is_deleted=models.BooleanField(default=False)
    def __str__(self) -> str:
         return self.name
     
class product(models.Model):
    img=models.ImageField( upload_to='pics', height_field=None, width_field=None, max_length=500,null=True)
    rearimg=models.ImageField( upload_to='pics', height_field=None, width_field=None, max_length=500,null=True)
    frontimg=models.ImageField( upload_to='pics', height_field=None, width_field=None, max_length=500,null=True)
    name=models.CharField(max_length=255)
    discription=models.TextField()
    category=models.ForeignKey(category, on_delete=models.CASCADE)
    size=models.ManyToManyField(Size)
    brand=models.ForeignKey(brand, on_delete=models.CASCADE)
    gender=models.CharField(max_length=10)
    price=models.IntegerField()
    disc_price=models.IntegerField(("discount price"),default=0)
    is_deleted=models.BooleanField(default=False)
    in_stock=models.IntegerField(null='not in stock')
    arrival_time=models.DateTimeField(default=timezone.now)

    

    def __str__(self) -> str:
        return self.name
    


    


    
    
    
