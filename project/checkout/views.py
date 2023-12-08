from django.shortcuts import render,redirect
from app.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from user.models import *
from django.db.models import Sum,F
from django.urls import reverse
from .models import *
import razorpay 
from django.dispatch import receiver
from .signals import order_created_signal
from django.core.mail import send_mail
from django.http import JsonResponse,HttpResponse,Http404
import json
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings




# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def checkout(request,id):
    user = request.user
    cartitems=cartitem.objects.all().filter(user=user,is_deleted=False)
    orderitems=ordereditems.objects.get(id=id)
    cart_instance = orderitems.items.all()
    total=orderitems.total
    districts = district.objects.all()
    prev_address = address.objects.filter(user=user)
    
    if request.method == 'POST':
        prev_address_id = request.POST.get('previous_address')
       
        if prev_address_id:
            # User selected a previous address
            prev_address = address.objects.get(id=prev_address_id)
            request.session['selected_address_id'] = prev_address_id
            return redirect(payment_view,id=orderitems.id)  # You may want to pass prev_address to the payment page
        else:
            # User is providing a new address
            name = request.POST.get('fullname')
            phone_number = request.POST.get('phone_number')
            user_district = request.POST.get('district')
            streetaddress = request.POST.get('streetaddress')
            pin = request.POST.get('pin')
            x = district.objects.get(id=user_district)
            y=address.objects.create(user=user, full_name=name, district=x, street_address=streetaddress, phone_number=phone_number, pin=pin)
            request.session['selected_address_id'] = y.id
            return redirect(payment_view,id=orderitems.id) 
    return render(request, 'checkout.html', {'cart_instance':cart_instance,'total':total,'districts':districts,'prev_address':prev_address,'ordereditem':orderitems})
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def user_address(request):
    #data to display in the page
    user = request.user
    districts = district.objects.all()
    prev_address = address.objects.filter(user=user)
    items = cartitem.objects.all().filter(is_deleted=False,user=user)
    total=float(items.aggregate(total=Sum('price'))['total'])
    
#getting adrresses of users
    if request.method == 'POST':
        prev_address_id = request.POST.get('previous_address')
        
        if prev_address_id:
            # User selected a previous address
            prev_address = address.objects.get(id=prev_address_id)
            request.session['selected_address_id'] = prev_address_id
            return redirect(payment_view)  # You may want to pass prev_address to the payment page
        else:
            # User is providing a new address
            name = request.POST.get('fullname')
            phone_number = request.POST.get('phone_number')
            user_district = request.POST.get('district')
            streetaddress = request.POST.get('streetaddress')
            pin = request.POST.get('pin')
            x = district.objects.get(id=user_district)
            y=address.objects.create(user=user, full_name=name, district=x, street_address=streetaddress, phone_number=phone_number, pin=pin)
            request.session['selected_address_id'] = y.id
           
            return redirect(payment_view) 

    return render(request,'confirmation.html',{'data':items,'districts':districts,'prev_address':prev_address,'total':total})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def payment_view(request,id):
    user=request.user
    addresss=request.session.get('selected_address_id')
    orderitems=ordereditems.objects.get(id=id)
    items=orderitems.items.all()
    total_price = orderitems.total
    walet=wallet.objects.get(user=user)
    to_pay=total_price*100
    wallet_option=walet.money>=total_price
    coupons=coupon.objects.all()
    usedcoupons=usercoupon.objects.filter(user=user)
     # Replace 'order_details' with your actual URL name
    success_url = request.build_absolute_uri(reverse('create_order', kwargs={'id': orderitems.id}))
    # failed_url = request.build_absolute_uri(reverse('payment-failed'))

    return render(request, 'payment.html', {'ordereditems':orderitems,'items':items,'total':total_price,'to_pay':to_pay,'success_url':success_url,'wallet_option':wallet_option,'coupons':coupons,'usedcoupons':usedcoupons})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def create_order(request,id):
    orderitems=ordereditems.objects.get(id=id)
    user=orderitems.user
    user_mail=user.email
    items=orderitems.items.all()
    total=Decimal(orderitems.total)
    adress=request.session.get('selected_address_id')
    deliver_address=address.objects.get(id=adress)
    

    order=Order.objects.create(user=user,address=deliver_address,payment="Paid",items=orderitems,total=total,order_status="Processing")
    send_mail(
                'Order confirmed',
                f' Your Order number: {order.id} from street trends has been confirmed .. will be dellivered in a few.. Thank You for shopping with streetrends',
                'streetrends@gmail.com',
                [user_mail],
                fail_silently=False,
            )
    for i in items:
        i.product.in_stock-=i.quantity
        i.product.save()
    order.save()
    return redirect(orders)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def walletpayment(request,id):
    user=request.user
    orderitems=ordereditems.objects.get(id=id)
    items=orderitems.items.all()
    walet=wallet.objects.get(user=user)
    total_price = orderitems.total
    walet.money-=total_price
    walet.save()
    adress=request.session.get('selected_address_id')
    deliver_address=address.objects.get(id=adress)
    
    if orderitems.coupon_applied==True:
        coupons=coupon.objects.get(name=request.session.get('coupon'))
        usercoupon.objects.create(user=user,coupon=coupons,used_at=timezone.now())
    orderr=Order.objects.create(user=user,created_at=timezone.now(),address=deliver_address,payment="Paid",items=orderitems,total=total_price,order_status="Processing")
    for product in items:
        product.product.in_stock-=product.quantity
        product.product.save()
    orderr.save() 
    return redirect(orders)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def cod(request,id):
    user=request.user
    orderitems=ordereditems.objects.get(id=id)
    items=orderitems.items.all()
    walet=wallet.objects.get(user=user)
    total_price = orderitems.total
    adress=request.session.get('selected_address_id')
    deliver_address=address.objects.get(id=adress)
    
    if orderitems.coupon_applied==True:
        coupons=coupon.objects.get(name=request.session.get('coupon'))
        usercoupon.objects.create(user=user,coupon=coupons,used_at=timezone.now())
    orderr=Order.objects.create(user=user,created_at=timezone.now(),address=deliver_address,payment="COD",items=orderitems,total=total_price,order_status="Processing")
    for product in items:
        product.product.in_stock-=product.quantity
        product.product.save()
    orderr.save()
    
    return redirect(orders)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def order_details(request,id):
   order= Order.objects.get(id=id)
   items=order.items.all()
   return render(request,'order_details.html',{'order':order,'items':items})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def orders(request):
   user=request.user
   order= Order.objects.filter(user=user).order_by('-created_at')
   return render(request,'order_status.html',{'data':order,'user':user})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def order_items(request,id):
    order=Order.objects.get(id=id)
    items=order.items.items.all()
    total_price=order.total
    return render(request,'order_items.html',{'items':items,'total':total_price,'order':order})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def return_order(request,id):
    order=Order.objects.get(id=id)
    status="Returned"
    order.order_status=status
    order.save()
    items=order.items.items.all()
    user_balance=wallet.objects.get(user=order.user)
    user_balance.money+=order.total
    user_balance.save()

    for i in items:
        product=i.product
        product.in_stock+=i.quantity
        product.save()

    user_mail=order.user.email
    send_mail(
                'Order cancelled',
                f' Your Order number: {order.id} from street trends has been requested to return\n Amount {order.total} has been refunded to your wallet..',
                'streetrends@gmail.com',
                [user_mail],
                fail_silently=False,
            )

    return redirect(orders)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userlogin')
def cancel_order(request,id):
    order=Order.objects.get(id=id)
    status="Cancelled"
    order.order_status=status
    order.save()
    items=order.items.items.all()
    user_balance=wallet.objects.get(user=order.user)
    user_balance.money+=order.total
    user_balance.save()

    for i in items:
        product=i.product
        product.in_stock+=i.quantity
        product.save()

    user_mail=order.user.email
    send_mail(
                'Order cancelled',
                f' Your Order number: {order.id} from street trends has been cancelled\n Amount {order.total} has been refunded to your wallet..',
                'streetrends@gmail.com',
                [user_mail],
                fail_silently=False,
            )

    return redirect(orders)

def add_to_wishlistt(request,id):
    user=request.user
    product_to_add=product.objects.get(id=id)
    wish,created=wishlist.objects.get_or_create(user=user)
    wish.items.add(product_to_add)
    return redirect('shop')

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
    return render(request,'wishlist.html',{'data':data})

def add_to_cart(request,id):
     user=request.user
     wishh=wishlist.objects.get(user=user)
     productt = product.objects.get(id=id)
     size_id = 1 
     size = Size.objects.get(id=size_id)
     item, created = cartitem.objects.get_or_create(product=productt, size=size,user=user,is_deleted=False)
     item.quantity = 1
     item.price=productt.price
     item.save()
     wishh.items.remove(productt)
     return redirect('viewcart')

def checkcoupon(request):
    user=request.user
    if request.method == 'POST':
        gift_code = request.POST.get('gift_code')
        orderid = request.POST.get('order_id')
        coupons=coupon.objects.filter(name=gift_code,valid_to__gte=timezone.now()).first()
        couponusage=usercoupon.objects.filter(user=user,coupon__name=coupons.name)
        
        # Your coupon processing logic here
        if not couponusage.exists():
            if coupons is not None:
                orderitems=ordereditems.objects.get(id=int(orderid))
                if orderitems.total>500:
                    if orderitems.coupon_applied==False:
                        request.session['coupon']=coupons.name
                        orderitems.total-=(coupons.discount_percentage/100)*orderitems.total 
                        orderitems.coupon_applied=True
                        orderitems.save() # Replace with your actual coupon code check
                        return JsonResponse({'success': True,'message': 'Coupon applied','updated_total': orderitems.total})
                    else:
                       return JsonResponse({'success': False, 'message': 'Only 1 coupon for an order is applicable'})
                else:
                     return JsonResponse({'success': False, 'message': 'Order total must be greater than $500'})    
            else:
                 return JsonResponse({'success': False, 'message': 'Coupon does not exist'})
        else:    
            return JsonResponse({'success': False, 'message': 'Coupon already applied'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def orderinvoice(request,id):
                orders=Order.objects.get(id=id)
               
                items=orders.items.items.all()
                date=orders.created_at
                total=orders.total
                template = 'orderinvoicepdf.html'
                context = {'orders': orders, 'items': items,'date':date,'total':total}
                pdf_data = render_to_string(template, context)
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="sales_report_{timezone.now()}.pdf"'
                pisa.CreatePDF(pdf_data, dest=response)
                return response








    










