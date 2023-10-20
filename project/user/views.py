from django.shortcuts import render,redirect
from app.models import product,Size,customuser
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.http import HttpResponse
from .models import cart,cartitem
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.db.models import Sum
# from checkout.views import checkout




# Create your views here.
def landing_page(request):
    if request.user.is_authenticated:
        return redirect(shop)
    
    x=product.objects.filter(Q(gender=1) & (Q(category=1)|Q(category=2)) & Q(category__is_deleted=False) & Q(is_deleted=False))
    y=product.objects.filter(Q(gender=2) & (Q(category=1)|Q(category=2)) & Q(category__is_deleted=False) & Q(is_deleted=False))
    z=product.objects.filter(Q(category=3) & Q(is_deleted=False) & Q(category__is_deleted=False))

    return render(request,'userindex.html',{'men':x,'women':y,'acc':z})

def contact(request):
    return render(request,'contact.html')

def user_signup(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        name=request.POST['name']

        if len(password)<6:
            messages.info(request,"password must be of atleast 6 characters")
            return redirect(user_signup)
        elif customuser.objects.filter(email=email).exists():
            messages.info(request,"email already exists")
            return redirect(user_signup)
        else:
            user=customuser.objects.create_user(username=username,password=password,email=email,first_name=name)
            user.save()
            return redirect(user_login)
        
    return render(request,'usersignup.html')

def details(request,id):
    data=product.objects.get(id=id)
    size=Size.objects.all()
    similar_products=product.objects.filter(Q(category=data.category) & ~Q(id=data.id) )

    return render(request,'details.html',{'data':data,'size':size,'similarproducts':similar_products})

def user_login(request):
    if request.user.is_authenticated:
        return redirect(shop)
    
    
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)

        if user is not None and not user.is_deleted:
            login(request,user)
            return redirect(shop)
        else:
            messages.info(request,'invalid username or password')
    return render(request,'user-login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def shop(request):
     x=product.objects.filter(Q(gender=1) & (Q(category=1)|Q(category=2)) & Q(category__is_deleted=False) & Q(is_deleted=False))
     y=product.objects.filter(Q(gender=2) & (Q(category=1)|Q(category=2)) & Q(category__is_deleted=False) & Q(is_deleted=False))
     z=product.objects.filter(Q(category=3) & Q(is_deleted=False) & Q(category__is_deleted=False))
     return render(request,'mainpage.html',{'men':x,'women':y,'acc':z})
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def womens(request):
     x=product.objects.filter(Q(gender=2) & Q(category=1) & Q(category__is_deleted=False) & Q(is_deleted=False))
     y=product.objects.filter(Q(gender=2) & Q(category=2) & Q(category__is_deleted=False) & Q(is_deleted=False))
     z=product.objects.filter(Q(gender=2) & Q(category=3) & Q(category__is_deleted=False) & Q(is_deleted=False))
     return render(request,'womensproducts.html',{'tops':x,'lowers':y,'acc':z})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
@login_required(login_url=user_login)
def mens(request):
     x=product.objects.filter(Q(gender=1) & Q(category=1) &  Q(category__is_deleted=False) & Q(is_deleted=False))
     y=product.objects.filter(Q(gender=1) & Q(category=2) &  Q(category__is_deleted=False) & Q(is_deleted=False))
     z=product.objects.filter(Q(gender=1) & Q(category=3) &  Q(category__is_deleted=False) & Q(is_deleted=False))
     return render(request,'mensproduct.html',{'tops':x,'lowers':y,'acc':z})
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def accessories(request):
       x=product.objects.filter(Q(gender=1) & Q(category=3) & Q(category__is_deleted=False) & Q(is_deleted=False))
       y=product.objects.filter(Q(gender=2) & Q(category=3) & Q(category__is_deleted=False) & Q(is_deleted=False))
       return render(request,'accessories.html',{'mens':x,'womens':y,})
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def user_profile(request):
    if request.user.is_authenticated:
        return render(request,'userprofile.html')
    return redirect(user_login)

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(landing_page)
    return HttpResponse('page not found')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def product_details(request,id):
    
        data=product.objects.get(id=id)
        size=data.size.all()
        user=request.user
        similar_products=product.objects.filter(Q(category=data.category) & ~Q(id=data.id) & Q(gender=data.gender))
        

        if request.method == 'POST':
            user_cart, created = cart.objects.get_or_create(user=user)
            cart_item, created = cartitem.objects.get_or_create(cart=user_cart,product=data)
            size = request.POST.get('size')
            quantity = request.POST.get('quantity')
            size=Size.objects.get(id=size)
            cart_item.size=size
            cart_item.quantity=quantity
            cart_item.price=data.price*Decimal(quantity)
            cart_item.save()
            user_cart.items.add(cart_item)
            return redirect(viewcart)
        return render(request,'productdetails.html',{'data':data,'size':size,'similarproducts':similar_products})
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def viewcart(request):
    user=request.user
    user_cart,created=cart.objects.get_or_create(user=user)
    data=user_cart.items.all()
    total_price=cartitem.objects.aggregate(total=Sum('price'))['total']
         

    return render(request, 'viewcart.html',{'data':data,'totalprice':total_price})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def delete_from_orders(request,id):
        user = request.user
        user_cart = get_object_or_404(cart, user=user)
        product_to_remove = get_object_or_404(cartitem,id=id)
        

        # Remove the product from the user's cart
        user_cart.items.remove(product_to_remove)
        cartitem.objects.get(id=id).delete()

        return redirect(viewcart)


     








        

    
