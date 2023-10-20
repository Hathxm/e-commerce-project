from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class customuser(AbstractUser):
    is_deleted=models.BooleanField(default=False)


    
class Size(models.Model):
    sizze = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]
    size=models.CharField(max_length=50,choices=sizze)
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


    def __str__(self) -> str:
        return self.wear
    
class gender(models.Model):
     choice=[
        ('Men','Male'),
        ('Women','Female'),
        ]
     gender=models.CharField( max_length=50,choices=choice)

     def __str__(self) -> str:
         return self.gender
     
class brand(models.Model):
    name=models.CharField( max_length=50)
    def __str__(self) -> str:
         return self.name
     
class product(models.Model):
    img=models.ImageField( upload_to='pics', height_field=None, width_field=None, max_length=None,null=True)
    name=models.CharField( max_length=50)
    category=models.ForeignKey(category, on_delete=models.CASCADE)
    size=models.ManyToManyField(Size)
    brand=models.ForeignKey(brand, on_delete=models.CASCADE)
    gender=models.ForeignKey(gender, on_delete=models.PROTECT)
    price=models.IntegerField()
    disc_price=models.IntegerField(("discount price"),null=True)
    is_deleted=models.BooleanField(default=False)
    
    # insertion_time=models.DateTimeField(_(""), auto_now=False, auto_now_add=False)
    

    def __str__(self) -> str:
        return self.name