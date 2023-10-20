from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from app.models import category,product,brand,customuser,gender
from django.db.models import Q
from django.contrib import messages


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)


        if user is not None and user.is_superuser:
            login(request,user)
            return redirect(admin_dashboard)
        else:
            messages.info(request,'wrong credintials this page is not available for users')
    return render(request,'adminlogin.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_dashboard(request):
    if request.user.is_superuser:
        return render(request,'adminindex.html')
    return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_category(request):
    if request.user.is_superuser:
        data=category.objects.all()
        return render(request,'admincategory.html',{'data':data})
    return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_products(request):
    if request.user.is_superuser:
        data=product.objects.filter(category__is_deleted=False)
        product_brand=brand.objects.all()
        product_category=category.objects.filter(is_deleted=False)
        sex=gender.objects.all()
       


        if request.method=='POST':
         img=request.FILES['image']
         name=request.POST['name']
         price=request.POST['price']
         new_category=request.POST['category']
         new_brand=request.POST['brand']
         new_pro_gender=request.POST['gender']
         new_pro_gender_instance=gender.objects.get(id=new_pro_gender)
         category_instance = category.objects.get(id=new_category)
         brand_instance = brand.objects.get(id=new_brand)

         product_data=product(img=img,name=name,category=category_instance,brand=brand_instance,price=price,gender=new_pro_gender_instance)
         product_data.save()



        return render(request,'adminproduct.html',{'data':data,'brand':product_brand,'category':product_category,'sex':sex})
    return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_category(request):
    if request.user.is_superuser:
         if request.method=='POST':
            newcategory=request.POST['addcategoryfield']
            x=category(wear=newcategory)
            x.save()
            return redirect(admin_category)
         return render(request,'add_category.html')
    return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_product(request,id):
    if request.user.is_superuser:
     data=product.objects.get(id=id)
     product_brand=brand.objects.all()
     product_category=category.objects.filter(is_deleted=False)

   
     if request.method=='POST':
         img=request.FILES['image']
         name=request.POST['name']
         new_category=request.POST['category']
         new_brand=request.POST['brand']
         category_instance = category.objects.get(id=new_category)
         brand_instance = brand.objects.get(id=new_brand)

         


         data.name=name
         data.img=img
         data.category=category_instance
         data.brand=brand_instance

         
         


         data.save()
         return redirect(edit_product,id=data.id)
     return render (request,'edit_product.html',{'data':data,'brand':product_brand,'category':product_category})
    return redirect(admin_login)


def delete_product(request,id):
    if request.user.is_superuser:
        data=product.objects.get(id=id)
        data.is_deleted=True
        data.save()
        return redirect(admin_products)
    return redirect(admin_login)
    
    
def undelete_product(request,id):
    if request.user.is_superuser:
        data=product.objects.get(id=id)
        data.is_deleted=False
        data.save()
        return redirect(admin_products)
    return redirect(admin_login)
    
    


def delete_category(request,id):
    if request.user.is_superuser:
        data=category.objects.get(id=id)
        data.is_deleted=True
        data.save()
        return redirect(admin_category)
    return redirect(admin_login)
    
    
def undelete_category(request,id):
    if request.user.is_superuser:
        data=category.objects.get(id=id)
        data.is_deleted=False
        data.save()
        return redirect(admin_category)
    return redirect(admin_login)


def delete_user(request,id):
    if request.user.is_superuser:
        data=customuser.objects.get(id=id)
        data.is_deleted=True
        data.save()
        return redirect(user_handling)
    return redirect(admin_login)


def undelete_user(request,id):
    if request.user.is_superuser:
        data=customuser.objects.get(id=id)
        data.is_deleted=False
        data.save()
        return redirect(user_handling)
    return redirect(admin_login)
    
def user_handling(request):
    if request.user.is_superuser:
        data=customuser.objects.all()
        return render(request,'admin-user.html',{'data':data})
    return redirect(admin_login)

def admin_logout(request):
    if request.user.is_superuser:
        logout(request)
        return redirect(admin_login)
    return redirect(admin_login)




   
     
