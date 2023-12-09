from django.shortcuts import render,redirect
from app.models import *
from checkout.models import *
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.http import HttpResponse
from .models import *
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.db.models import *
from django.db.models.functions import Coalesce
from django.core.mail import send_mail
from random import randint
from django.contrib.auth.hashers import make_password
from django.db.models import F,ExpressionWrapper,FloatField
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string



# Create your views here.
def landing_page(request):
    if request.method=="POST":
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        message=request.POST['message']
        tocontact.objects.create(first_name=firstname,last_name=lastname,email=email,message=message)
        messages.info(request,"You will be contacted soon ..enjoy the shopping experience !")
        return redirect (landing_page)
    return render(request,'userindex.html')

def contact(request):
    if request.method=="POST":
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        message=request.POST['message']
        tocontact.objects.create(first_name=firstname,last_name=lastname,email=email,message=message)
        messages.info(request,"You will be contacted soon ..enjoy the shopping experience !")
    return render(request,'contact.html')

def user_signup(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        name=request.POST['name']
        
        if len(username)<6:
            messages.info(request,"username must be of atleast 6 characters")
        elif len(password)<8:
            messages.info(request,"password must be of atleast 8 characters")
            return redirect(user_signup)
        elif customuser.objects.filter(email=email).exists():
            messages.info(request,"email already exists")
            return redirect(user_signup)
        elif customuser.objects.filter(username=username).exists():
            messages.info(request,"username already taken")
            return redirect(user_signup)
        else:
             otp=randint(1000,9999)
             request.session['otp'] = otp
             request.session['otp_created_at'] = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
             request.session['username'] = username
             request.session['password'] = password
             request.session['email'] = email
             request.session['name'] = name


             send_mail(
                'Password Reset OTP',
                f'Your password for login is: {otp}',
                'streetrends@gmail.com',
                [email],
                fail_silently=False,
            )
             messages.success(request,'Your Signup Was Successful.. Enter Details with OTP sent to your mail')
             return redirect(OTP_login)
         
    return render(request,'usersignup.html')


def OTP_login(request):
     if request.user.is_authenticated:
        return redirect(shop)
     
     otpp=request.session.get('otp')
     username=request.session.get('username')
     email=request.session.get('email')
     password=request.session.get('password')
     name=request.session.get('name')

     otp_created_at_str = request.session.get('otp_created_at')
     otp_created_at = datetime.strptime(otp_created_at_str, "%Y-%m-%d %H:%M:%S")
     otp_created_at = timezone.make_aware(otp_created_at, timezone.get_current_timezone())

        # Check if OTP has expired (2 minutes duration)
     otp_expiry_duration = 2
     condition = (timezone.now() - otp_created_at).total_seconds() <= otp_expiry_duration * 60
     
     if request.method=="POST":
          otp=int(request.POST.get('otp'))
          if otp == otpp:
             user=customuser.objects.create_user(username=username,password=password,email=email,first_name=name)
             user_balance=wallet.objects.create(user=user)
             user_wishlist=wishlist.objects.create(user=user)
             return redirect(user_login)
          else:
               messages.info(request,'wrong otp')
               return redirect(OTP_login)
     return render(request,'otplogin.html',{'condition':condition})
          
               
def resend_otp(request):
     if request.method=="POST":
          email=request.session.get('email')
          otp=randint(1000,9999)
          request.session['otp'] = otp
          request.session['otp_created_at'] = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
          send_mail(
                'Password login OTP',
                f'Your password for login is: {otp}',
                'streetrends@gmail.com',
                [email],
                fail_silently=False,
            )
          return redirect(OTP_login)


             


def user_login(request):
    if request.user.is_authenticated:
        return redirect(shop)
    

    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)

        if user is not None and not user.is_deleted :
                   login(request,user)
                   return redirect(shop)
        else:
                   messages.info(request,'invalid username or password')
        
    return render(request,'user-login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def details(request,id):
    data=product.objects.get(id=id)
    size=Size.objects.all()
    similar_products=product.objects.filter(Q(category=data.category) & ~Q(id=data.id))

    if request.method=="POST":
         return redirect(user_login)

    return render(request,'single.html',{'data':data,'size':size,'similarproducts':similar_products})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def shop(request):
     user=request.user
     now=timezone.now()
     x=product.objects.filter(Q(gender="Men") & (Q(category__wear="Tops")|Q(category__wear="Lowers")) & Q(category__is_deleted=False) & Q(is_deleted=False) & Q(brand__is_deleted=False)).annotate(amt=F('price') - F('disc_price'),cat_off=F('price') - (F('price') * F('category__discount_percentage') / 100),cat_amt=F('price')-(F('price') - (F('price') * F('category__discount_percentage') / 100))).order_by('name')
     y=product.objects.filter(Q(gender="Women") &  (Q(category__wear="Tops")|Q(category__wear="Lowers")) & Q(category__is_deleted=False) & Q(is_deleted=False)  &Q(brand__is_deleted=False)).annotate(amt=F('price') - F('disc_price'),cat_off=F('price') - (F('price') * F('category__discount_percentage') / 100),cat_amt=F('price')-(F('price') - (F('price') * F('category__discount_percentage') / 100))).order_by('name')
     z=product.objects.filter(Q(category__wear="Accessories") & Q(is_deleted=False) & Q(category__is_deleted=False) & Q(brand__is_deleted=False)).annotate(amt=F('price')-F('disc_price'),cat_off=F('price') - (F('price') * F('category__discount_percentage') / 100),cat_amt=F('price')-(F('price') - (F('price') * F('category__discount_percentage') / 100))).order_by('name')
     wish= wishlist.objects.get(user=user)
     items=wish.items.all() 
   
     products_you_may_like = cartitem.objects.filter(user=user,product__brand__is_deleted=False).distinct('product').annotate(
     amt=F('product__price') - F('product__disc_price'),
     cat_off=F('product__price') - F('product__price') * F('product__category__discount_percentage') / 100,
     cat_amt=F('product__price') - (F('product__price') - F('product__price') * F('product__category__discount_percentage') / 100))
     return render(request,'mainpage.html',{'men':x,'women':y,'acc':z,'wish':items,'now':now,'products_you_may_like':products_you_may_like})
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def womens(request):
    user = request.user
    search_term = request.GET.get('search')
    sort_option = request.POST.get('sortSelect')
    now=timezone.now()

    if search_term:
        # If a search term is present, filter products based on the search term,
        x = product.objects.filter(Q(gender="women") & Q(category__wear="Tops") & Q(category__is_deleted=False) & Q(is_deleted=False) & Q(name__icontains=search_term) &Q(brand__is_deleted=False)).annotate(amt=F('price') - F('disc_price'),cat_off=F('price') - (F('price') * F('category__discount_percentage') / 100),cat_amt=F('price')-(F('price') - (F('price') * F('category__discount_percentage') / 100)))
        y = product.objects.filter(Q(gender="Women") & Q(category__wear="Lowers") & Q(category__is_deleted=False) & Q(is_deleted=False) & Q(name__icontains=search_term) &Q(brand__is_deleted=False)).annotate(amt=F('price') - F('disc_price'),cat_off=F('price') - (F('price') * F('category__discount_percentage') / 100),cat_amt=F('price')-(F('price') - (F('price') * F('category__discount_percentage') / 100)))
        z = product.objects.filter(Q(gender="Women") & Q(category__wear="Accessories") & Q(category__is_deleted=False) & Q(is_deleted=False) & Q(name__icontains=search_term) &Q(brand__is_deleted=False)).annotate(amt=F('price') - F('disc_price'),cat_off=F('price') - (F('price') * F('category__discount_percentage') / 100),cat_amt=F('price')-(F('price') - (F('price') * F('category__discount_percentage') / 100)))
    else:
        # If no search term, use the original queryset
        x = product.objects.filter(Q(gender="Women") & Q(category__wear="Tops") & Q(category__is_deleted=False) & Q(is_deleted=False) &Q(brand__is_deleted=False)).annotate(amt=F('price') - F('disc_price'),cat_off=F('price') - (F('price') * F('category__discount_percentage') / 100),cat_amt=F('price')-(F('price') - (F('price') * F('category__discount_percentage') / 100)))
        y = product.objects.filter(Q(gender="Women") & Q(category__wear="Lowers") & Q(category__is_deleted=False) & Q(is_deleted=False) &Q(brand__is_deleted=False)).annotate(amt=F('price') - F('disc_price'),cat_off=F('price') - (F('price') * F('category__discount_percentage') / 100),cat_amt=F('price')-(F('price') - (F('price') * F('category__discount_percentage') / 100)))
        z = product.objects.filter(Q(gender="Women") & Q(category__wear="Accessories") & Q(category__is_deleted=False) & Q(is_deleted=False) &Q(brand__is_deleted=False)).annotate(amt=F('price') - F('disc_price'),cat_off=F('price') - (F('price') * F('category__discount_percentage') / 100),cat_amt=F('price')-(F('price') - (F('price') * F('category__discount_percentage') / 100)))
       

    
# Apply the sorting individually for each queryset
    if sort_option == 'low_to_high':
        x = x.order_by(F('disc_price'))
        y = y.order_by(F('disc_price'))
        z = z.order_by(F('disc_price'))
    elif sort_option == 'high_to_low':
         x = x.order_by('-disc_price')
         y = y.order_by('-disc_price')
         z = z.order_by('-disc_price')

    wishlist_obj = wishlist.objects.get(user=user)
    wish = wishlist_obj.items.all()
    

    return render(request, 'womensproducts.html', {'tops': x, 'lowers': y, 'acc': z, 'wish': wish,'now':now})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
@login_required(login_url=user_login)
def mens(request):
     user = request.user
     search_term = request.GET.get('search')
     sort_option = request.POST.get('sortSelect')
     now=timezone.now()

     if search_term:
        # If a search term is present, filter products based on the search term
         x = product.objects.filter(Q(gender="Men") & Q(category__wear="Tops") & Q(category__is_deleted=False) & Q(is_deleted=False) & Q(name__icontains=search_term) &Q(brand__is_deleted=False)).annotate(amt=F('price') - F('disc_price'))
         y = product.objects.filter(Q(gender="Men") & Q(category__wear="Lowers") & Q(category__is_deleted=False) & Q(is_deleted=False) & Q(name__icontains=search_term) &Q(brand__is_deleted=False)).annotate(amt=F('price') - F('disc_price'))
         z = product.objects.filter(Q(gender="Men") & Q(category__wear="Accessories") & Q(category__is_deleted=False) & Q(is_deleted=False) & Q(name__icontains=search_term) &Q(brand__is_deleted=False)).annotate(amt=F('price') - F('disc_price'))
     else:
        # If no search term, use the original queryset
        x = product.objects.filter(Q(gender="Men") & Q(category__wear="Tops") & Q(category__is_deleted=False) & Q(is_deleted=False) &Q(brand__is_deleted=False)).annotate(amt=F('price') - F('disc_price'),cat_off=F('price') - (F('price') * F('category__discount_percentage') / 100),cat_amt=F('price')-(F('price') - (F('price') * F('category__discount_percentage') / 100)))
        y = product.objects.filter(Q(gender="Men") & Q(category__wear="Lowers") & Q(category__is_deleted=False) & Q(is_deleted=False) &Q(brand__is_deleted=False)).annotate(amt=F('price') - F('disc_price'),cat_off=F('price') - (F('price') * F('category__discount_percentage') / 100),cat_amt=F('price')-(F('price') - (F('price') * F('category__discount_percentage') / 100)))
        z = product.objects.filter(Q(gender="Men") & Q(category__wear="Accessories") & Q(category__is_deleted=False) & Q(is_deleted=False) &Q(brand__is_deleted=False)).annotate(amt=F('price') - F('disc_price'),cat_off=F('price') - (F('price') * F('category__discount_percentage') / 100),cat_amt=F('price')-(F('price') - (F('price') * F('category__discount_percentage') / 100)))

     if sort_option == 'low_to_high':
        x = x.order_by(F('disc_price'))
        y = y.order_by(F('disc_price'))
        z = z.order_by(F('disc_price'))
     elif sort_option == 'high_to_low':
         x = x.order_by('-disc_price')
         y = y.order_by('-disc_price')
         z = z.order_by('-disc_price')



     wishlist_obj = wishlist.objects.get(user=user)
     wish = wishlist_obj.items.all()
     return render(request,'mensproduct.html',{'tops':x,'lowers':y,'acc':z,'wish':wish,'now':now})
   
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def accessories(request):
    user = request.user
    search_term = request.GET.get('search')
    sort_option = request.POST.get('sortSelect')
    now = timezone.now()

    base_query = Q(category__name="Accessories") & Q(category__is_deleted=False) & Q(is_deleted=False) & Q(brand__is_deleted=False)

    if search_term:
        x = product.objects.filter(Q(gender="Men") & base_query & Q(name__icontains=search_term)).annotate(amt=F('price') - F('disc_price'))
        y = product.objects.filter(Q(gender="Women") & base_query & Q(name__icontains=search_term)).annotate(amt=F('price') - F('disc_price'))
    else:
        x = product.objects.filter(Q(gender="Men") & base_query).annotate(amt=F('price') - F('disc_price'))
        y = product.objects.filter(Q(gender="Women") & base_query).annotate(amt=F('price') - F('disc_price'))

    if sort_option == 'low_to_high':
        x = x.order_by('disc_price')
        y = y.order_by('disc_price')
    elif sort_option == 'high_to_low':
        x = x.order_by('-disc_price')
        y = y.order_by('-disc_price')

    # Rest of your code...

    return render(request, 'your_template.html', {'x': x, 'y': y, 'other_context_variables': 'values'})
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def user_profile(request):
     user=request.user
     user_address=address.objects.filter(user=user)
     balance=wallet.objects.get(user=user)
     return render(request,'userprofile.html',{'user_address':user_address,'user_balance':balance})



def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(landing_page)
    return HttpResponse('page not found')


    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def viewcart(request):
    user = request.user
    cart_items = cartitem.objects.all().filter(is_deleted=False, user=user)
    total_price = cart_items.aggregate(total=Sum('price'))['total']
    out_of_stock = []
    item_count=cart_items.count()
    if total_price is None:
         total_price=0

    if request.method == 'POST':
        for item in cart_items:
            quantity_key = f'quantity_{item.id}'
            new_quantity = int(request.POST.get(quantity_key))
            product_items = cartitem.objects.filter(product=item.product, is_deleted=False, user=user)

            #restricting total of product with different sizes
            total_quantity = product_items.aggregate(qty=Sum('quantity'))['qty']

            if total_quantity > item.product.in_stock: 
                messages.info(request, f'{item.product} quantity demanded not in stock')
                return redirect('viewcart')

            if new_quantity >= 0:
                if new_quantity <= item.product.in_stock:
                    item.quantity = new_quantity 
                else:
                    out_of_stock.append(item)
            else:
                messages.error(request, "Invalid quantity.")

        if len(out_of_stock) > 0:
            product_names = ', '.join([str(item.product) for item in out_of_stock])
            messages.warning(request, f'Items out of stock: {product_names}')
        elif not cart_items.exists():
            messages.warning(request, 'No items selected')
        else:
            orderitems = ordereditems.objects.create(user=user)
            for item in cart_items:
                # Use the updated price for each item
                 # Refresh the item to get the updated price
                orderitems.items.add(item)
                orderitems.save()
            
            # Use the total_price calculated from updated prices
            orderitems.total = total_price
            orderitems.save()

            messages.success(request, "Cart updated successfully.")
            return redirect('checkout', id=orderitems.id)

    return render(request, 'viewcart.html', {'data': cart_items, 'user': user, 'total': total_price,'item_count': item_count})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def delete_from_orders(request,id):
        item=cartitem.objects.get(id=id)
        item.is_deleted=True
        item.save()
        return redirect(viewcart)

def forgot_password(request):
     if request.method=='POST':
          email=request.POST.get('email')


          if customuser.objects.filter(email=email).exists():
               request.session['email']=email
               user=customuser.objects.get(email=email)
               otp=randint(1000,9999)
               user.otp=otp
               user.otp_created_at=timezone.now()
               user.save()
               send_mail(
                'Password Reset OTP',
                f'Your OTP for password reset is: {otp}',
                'streetrends@gmail.com',
                [email],
                fail_silently=False,
            )
               return redirect(verify_otp)
          else:
               messages.info(request,'user with email doesnt exist')
               
     return render(request,'forgot_pass.html')


def verify_otp(request):
     email=request.session.get('email')
     user=customuser.objects.get(email=email)
     current_time=timezone.now()
     otp_expiry_duration=2
     condition=(current_time - user.otp_created_at).total_seconds()<= otp_expiry_duration * 60

     if request.method=='POST':
          otp=int(request.POST.get('otp'))
          password=request.POST.get('password')
          confirm_pass=request.POST.get('confirm_pass')
          if otp==user.otp:
               if condition:
                    if password==confirm_pass:
                         user.password=make_password(password)
                         user.save()
                         return redirect(user_login)
                    else:
                     messages.info(request,'password doesnt match')
               else:
                     messages.info(request,'OTP expired')
          else:
                    messages.info(request,'invalid otp')
                    
     return render(request,'verifyotp.html',{'condition':condition})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def product_details(request,id):
     data=product.objects.get(id=id)
     size=data.size.all()
     user=request.user
     wishilistt=wishlist.objects.get(user=user)
     wish=wishilistt.items.all()
     similar_products=product.objects.filter(Q(category=data.category) & ~Q(id=data.id)).annotate(amt=F('price') - F('disc_price'),cat_off=F('price') - (F('price') * F('category__discount_percentage') / 100),cat_amt=F('price')-(F('price') - (F('price') * F('category__discount_percentage') / 100))).order_by('name')
     cat_off_price=data.price-(data.price*data.category.discount_percentage/100)
     now=timezone.now()

     if data.in_stock==0:
                messages.warning(request,'Product not in stock')

     if request.method == 'POST':
              size = request.POST.get('size')
              size=Size.objects.get(id=size)
              cart_item,created=cartitem.objects.get_or_create(product=data,user=user,size=size,is_deleted=False)
              quantity = int(request.POST.get('quantity'))
              cart_item.quantity=quantity

              if quantity>data.in_stock:
                 messages.warning(request,'Quantity demanded not in stock')
                 return redirect(product_details,id=data.id)
                 
              cart_item.price=data.disc_price*(quantity)+(cart_item.size.price_increment*quantity)
              cart_item.save()
              return redirect(viewcart)
     return render(request,'single.html',{'data':data,'size':size,'similar_products':similar_products,'wish':wish,'cat_off_price':cat_off_price,'now':now})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def edit_profile(request):
     user=request.user.username
     user=customuser.objects.get(username=user)
     addres=address.objects.filter(user=user)

     if request.method=="POST":
          if 'image' in request.FILES:
               user_img=request.FILES['image']
               user.user_img=user_img
          elif user.user_img:
               user_img=user.user_img
          else:
               user_img=None 
          first_name=request.POST.get('firstname')
          last_name=request.POST.get('lastname')
          new_addres=request.POST.get('address')
          email=request.POST.get('email')
          phone_number=request.POST.get('phone_number')


          user.first_name = first_name
          user.last_name = last_name
          user.email = email
        
          user.phone_number = phone_number
          user.user_img=user_img

          user.save()
          return redirect(user_profile)

     return render(request,'editprofile.html',{'user':user,'address':addres})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
@login_required(login_url=user_login)
def add_to_wishlistt(request,id):
    user=request.user
    product_to_add=product.objects.get(id=id)
    wish,created=wishlist.objects.get_or_create(user=user)
    wish.items.add(product_to_add)
    return redirect('shop')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
@login_required(login_url=user_login)
def dlt_from_wishlist(request,id):
    user=request.user
    product_to_dlt=product.objects.get(id=id)
    wishlistt=wishlist.objects.get(user=user)
    wishlistt.items.remove(product_to_dlt)
    return redirect('shop')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def view_wishlist(request):
    user=request.user
    wishlistt=wishlist.objects.get(user=user)
    data=wishlistt.items.all().annotate(amt=F('price')-F('disc_price'))
    products_you_may_like = cartitem.objects.filter(user=user,product__brand__is_deleted=False).distinct('product').annotate(
    amt=F('product__price') - F('product__disc_price'),
    cat_off=F('product__price') - F('product__price') * F('product__category__discount_percentage') / 100,
    cat_amt=F('product__price') - (F('product__price') - F('product__price') * F('product__category__discount_percentage') / 100))
    return render(request,'wishlist.html',{'data':data,'products_you_may_like':products_you_may_like})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def add_to_cart(request,id):
     user=request.user
     product_instance = get_object_or_404(product, id=id)

    # Assuming product has a many-to-many relationship with size
    # If size is a ForeignKey, adjust accordingly
     sizes = product_instance.size.all()

    # For simplicity, consider the first size from the available sizes
     if sizes.exists():
        size = sizes.first()
     else:
        # Handle the case where the product has no size
        size = None

     item, created = cartitem.objects.get_or_create(
        product=product_instance,
        size=size,
        user=user,
        is_deleted=False
    )

     item.quantity = 1
     item.price = product_instance.disc_price + (size.price_increment if size else 0)
     item.save()
 
     return redirect('viewcart')

def qty_update(request):
    user = request.user
    item_id = request.POST.get('item_id')
    new_quantity = int(request.POST.get('new_quantity'))

    cart_item = get_object_or_404(cartitem, id=item_id)
    now=timezone.now()

    # Update the quantity in the database
    cart_item.quantity = new_quantity
    cart_item.price = (cart_item.product.disc_price * new_quantity) + (cart_item.size.price_increment * new_quantity)
    cart_item.save()

    # You can optionally return some data in the response
    response_data = {'new_qty':new_quantity,'new_price':cart_item.price}
    return JsonResponse(response_data)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
@login_required(login_url=user_login)
def delete(request):
     user=request.user
     response_data = {'wish':0,'message':'item already in wishlist'}
     return JsonResponse(response_data)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
@login_required(login_url=user_login)
def add(request):
    user = request.user
    item_id = request.POST.get('item_id')
    wish = wishlist.objects.get(user=user)
    item = wish.items.all()
    product_id=product.objects.get(id=item_id)
    

    if product_id in item:
        response_data = {
            'wish': 1,
            'message': 'item already in wishlist'
        }
        return JsonResponse(response_data)

    wish.items.add(product_id)
    wish.save()
    response_data = {
        'wish': 1,
        'message': 'item added successfully'
    }
    return JsonResponse(response_data)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
@login_required(login_url=user_login)
def size_variation(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        item = product.objects.filter(id=id).annotate(amt=F('price') - F('disc_price')).first()
        user_size = request.POST.get('size')
        size=Size.objects.get(id=user_size)
        now=timezone.now()
        
        if item.disc_price != 0:
            item_price=item.disc_price+size.price_increment
        else:
            item_price=item.price+size.price_increment  
        return JsonResponse({'status': 'success','price':item_price})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

     





     

     








        

    
