from django.shortcuts import render,redirect
from app.models import product,Size,customuser
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from decimal import Decimal
from user.models import cart,cartitem,item_status
from django.db.models import Sum
from user.views import user_login
from .models import address,district,Order,payment_method,order_status

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def checkout(request):
    user = request.user
    cart_instance = cart.objects.get(user=user)
    data = cart_instance.items.all()
    total = data.aggregate(total=Sum('price'))['total']

    

    # Create a new order or retrieve an existing one
    if Order.objects.filter(user=user).exists():
        order = Order.objects.get(user=user)
        status=order_status.objects.get(id=5)
        order.order_status=status
        order.save()
    else:
        order = Order.objects.create(user=user)

    # Associate cart items with the order
    for cart_item in data:
        order.items.add(cart_item)

    # Clear the cart items
    cart_instance.delete()
    return render(request, 'checkout.html', {'data': data, 'total': total})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def confirmation(request):
    user = request.user
    purchased_items = Order.objects.get(user=user)
    data = purchased_items.items.filter(status=3)
    total_price = data.aggregate(total=Sum('price'))['total']
    districts = district.objects.all()
    prev_address = address.objects.filter(user=user)
    

    if request.method == 'POST':
        prev_address_id = request.POST.get('previous_address')

        if prev_address_id:
            # User selected a previous address
            prev_address = address.objects.get(id=prev_address_id)
            purchased_items.address=prev_address
            purchased_items.save()
            return redirect('payment')  # You may want to pass prev_address to the payment page
        else:
            # User is providing a new address
            name = request.POST.get('fullname')
            phone_number = request.POST.get('phone_number')
            user_district = request.POST.get('district')
            streetaddress = request.POST.get('streetaddress')
            pin = request.POST.get('pin')
            x = district.objects.get(id=user_district)
            y=address.objects.create(user=user, full_name=name, district=x, street_address=streetaddress, phone_number=phone_number, pin=pin)
            purchased_items.address=y
            purchased_items.save()
            return redirect('payment')

    return render(request, 'confirmation.html', {
        'data': data,
        'total': total_price,
        'districts': districts,
        'prev_address': prev_address,
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def payment_view(request):
     data=payment_method.objects.all()
     order=Order.objects.get(user=request.user)
     items=order.items.filter(status=3)
     if request.method=="POST":
         payment=request.POST.get('payment_option')
         pay=payment_method.objects.get(id=payment)
         order.payment=pay
         order.save()
         return redirect(order_confirmed)
     return render(request,'payment.html',{'data':data,'items':items})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def order_confirmed(request):
    order=Order.objects.get(user=request.user)
    items=order.items.filter(status=3)
    return render(request,'order_confirm.html',{'order':order,'items':items})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def cancel_item(request,id):
    x=cartitem.objects.get(id=id)
    canceled_status = item_status.objects.get(id=4)
    x.status=canceled_status
    x.save()
    return redirect(orderr_status)

def return_item(request,id):
    x=cartitem.objects.get(id=id)
    return_status = item_status.objects.get(id=1)
    x.status=return_status
    x.save()
    return redirect(orderr_status)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def orderr_status(request):
    order=Order.objects.get(user=request.user)
    return render(request,'order_status.html',{'order':order})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def cancel_order(request,order_id):
    # Fetch the order to be canceled
    order = get_object_or_404(Order, id=order_id)
    status=order_status.objects.get(id=4)
    order.order_status=status
    order.save()
    items=order.items.all()
    itemstatus=item_status.objects.get(id=4)
    for i in items:
        i.status=itemstatus
        i.save()
    # Redirect to the order status page
    return redirect('order_status')


