from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from app.models import *
from django.db.models import Q
from django.contrib import messages
from checkout.models import *
from django.http import HttpResponse,JsonResponse
from user.models import *
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from django.db.models import Count, Sum, Case, When, Value, IntegerField, F, ExpressionWrapper, fields
from django.utils import timezone
from .resources import OrderResource
from xhtml2pdf import pisa
from django.template.loader import render_to_string


# Create your views here.

def admin_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)


        if user is not None and user.is_superuser:
            login(request,user)
            wallet.objects.get_or_create (user=user)
            wishlist.objects.get_or_create(user=user)
            return redirect(admin_dashboard)
        else:
            messages.info(request,'wrong credintials this page is not available for users')
    return render(request,'adminlogin.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def admin_dashboard(request): 
     if request.user.is_superuser:
        selected_year = timezone.now().year
        if request.method == "POST": 
            selected_year = int(request.POST.get('year'))

        # Filter orders based on the selected year
        orders_query = Order.objects.filter(created_at__year=selected_year)

        # Query to get monthly order counts
        queryset = orders_query.annotate(month=TruncMonth('created_at')).values('month').annotate(order_count=Count('id'))

        # Total sales for the selected year
        total_sales = orders_query.aggregate(total_amount=Sum('total'))['total_amount']
        if total_sales is None:
            total_sales = 'No orders made in this year'

        # Calculate the percentage of online orders
        total_orders = orders_query.aggregate(total_orders=Count('id'))['total_orders']
        online_payment_percentage = 0.0
        if total_orders > 0:
            online_payment_percentage = orders_query.filter(payment="Paid").count() * 100 / total_orders

        # Calculate the percentage of COD orders
        cod_percentage = 0.0
        if total_orders > 0:
            cod_percentage = orders_query.filter(payment="COD").count() * 100 / total_orders

        paid_transactions = orders_query.filter(Q(payment="Paid") & (Q(order_status="Delivered") | Q(order_status="Processing")))
        cod_transactions = orders_query.filter(payment='COD',order_status="Delivered")
        labels = [entry['month'].strftime('%B %Y') for entry in queryset]
        data = [entry['order_count'] for entry in queryset]

        # Get recent orders (all orders for simplicity; adjust as needed)
        recent_orders = orders_query.order_by('-created_at')

        return render(request, 'adminindex.html', {
            'labels': labels,
            'data': data,
            'selected_year': selected_year,
            'total': total_sales,
            'recent_orders': recent_orders,
            'online_payment_percentage': online_payment_percentage,
            'cod':cod_percentage,
            'paid_transactions': paid_transactions,
            'cod_transactions': cod_transactions,
        })
     return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def userreviews(request):
    data=tocontact.objects.all()
    return render(request,'userreviews.html',{'data':data})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def admin_category(request):
    if request.user.is_superuser:
        data=category.objects.all()
        return render(request,'admincategory.html',{'data':data})
    return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def admin_brands(request):
    if request.user.is_superuser:
        data=brand.objects.all()
        return render(request,'adminbrand.html',{'data':data})
    return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def admin_size(request):
    if request.user.is_superuser:
        data=Size.objects.all()
        return render(request,'adminsize.html',{'data':data})
    return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def admin_coupons(request):
    if request.user.is_superuser:
        data=coupon.objects.all()
        return render(request,'admincoupons.html',{'data':data})
    return redirect(admin_login)


    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def admin_products(request):
    if request.user.is_superuser:
        data=product.objects.filter(category__is_deleted=False)
        product_brand=brand.objects.all()
        product_category=category.objects.filter(is_deleted=False)
        size=Size.objects.all()
       

        if request.method=='POST':
         img=request.FILES['image']
         rearimg=request.FILES['rearimage']
         frontimg=request.FILES['frontimage']
         name=request.POST['name']
         price=request.POST['price']
         disc_price = request.POST.get('disc_price')
         new_category=request.POST['category']
         new_brand=request.POST['brand']
         new_pro_gender=request.POST['gender']
         new_stock=request.POST['stock']
         discription=request.POST['discription']
         new_size=request.POST.getlist('size')

         if not disc_price:
             disc_price=0
         elif len(name)>20:
             messages.warning(request,"choose a shorter name for the product")
             return redirect(admin_products)
        
         
         category_instance = category.objects.get(id=new_category)
         brand_instance = brand.objects.get(id=new_brand)
         new_product=product.objects.create(img=img,name=name,rearimg=rearimg,frontimg=frontimg,category=category_instance,brand=brand_instance,price=price,disc_price=disc_price,gender=new_pro_gender,in_stock=new_stock,discription=discription)
         for size in new_size:
           new_product.size.add(size)
         new_product.save()
         return redirect(admin_products)
             
        
         
        return render(request,'adminproduct.html',{'data':data,'brand':product_brand,'category':product_category,'size':size})
    return redirect(admin_login)
   

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def add_category(request):
         if request.method=='POST':
            newcategory=request.POST['addcategoryfield']
            x=category(wear=newcategory)
            x.save()
            return redirect(admin_category)
         return render(request,'add_category.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def add_brand(request):
         if request.method=='POST':
            newbrand=request.POST['addcategoryfield']
            brand.objects.create(name=newbrand)
            return redirect(admin_brands)
         return render(request,'add_brand.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def add_size(request):
         if request.method=='POST':
            newsize=request.POST['addcategoryfield']
            price_increment=request.POST['priceincrement']
            Size.objects.create(size=newsize,price_increment=price_increment)
            return redirect(admin_size)
         return render(request,'add_size.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def add_coupons(request):
    if request.method == 'POST':
        coupons = request.POST.get('coupon')
        datetime_str = request.POST.get('datetime')
        discount_percentage = int(request.POST.get('disc_percentage'))

        # Convert the datetime string to a datetime object
        valid_to = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
        if discount_percentage>0 and discount_percentage<100:
            coupon.objects.create(name=coupons,valid_from=timezone.now(),valid_to=valid_to,discount_percentage=discount_percentage)
            return redirect(admin_coupons)
        else:
            messages.warning(request,"discount percentage cannot be greater than 100 or below 0")
    return render(request,'add_coupons.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def edit_product(request,id):
    if request.user.is_superuser:
     data=product.objects.get(id=id)
     product_brand=brand.objects.all()
     product_category=category.objects.filter(is_deleted=False)
    
     categoryy=category.objects.all()
     size=Size.objects.all()

   
     if request.method=='POST':
         img=request.FILES['image'] if 'image' in request.FILES else data.img
         rearimg=request.FILES['rearimage']  if 'rearimg' in request.FILES else data.rearimg
         frontimg=request.FILES['frontimage']  if 'frontimage' in request.FILES else data.frontimg
         name=request.POST['name']
         new_category=request.POST['category']
         selected_sizes = request.POST.getlist('size')
         sizes = [int(size_id) for size_id in selected_sizes]
         new_brand=request.POST['brand']
         new_price=request.POST['price']
         new_disc_price=request.POST['disc_price']
         new_stock=request.POST['stock']

         if float(new_disc_price) >= float(new_price):
             messages.info(request, 'Discount price should be less than the product price.')
             return redirect(edit_product)
         elif len(name)>20:
             messages.warning(request,"choose a shorter name for the product")
             return redirect(edit_product)


         category_instance = category.objects.get(id=new_category)
         brand_instance = brand.objects.get(id=new_brand)


         data.name=name
         data.img=img
         data.rearimg=rearimg
         data.frontimg=frontimg
         data.category=category_instance
         data.brand=brand_instance
         data.price=new_price
         for i in sizes:
             data.size.add(i)
         data.disc_price=new_disc_price
         data.in_stock=new_stock

         


         data.save()
         return redirect(edit_product,id=data.id)
     return render (request,'edit_product.html',{'data':data,'brand':product_brand,'category':product_category,'category':categoryy,'size':size})
    return redirect(admin_login)
   

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def delete_product(request,id):
    if request.user.is_superuser:
        data=product.objects.get(id=id)
        data.is_deleted=True
        data.save()
        return redirect(admin_products)
    return redirect(admin_login)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def undelete_product(request,id):
    if request.user.is_superuser:
        data=product.objects.get(id=id)
        data.is_deleted=False
        data.save()
        return redirect(admin_products)
    return redirect(admin_login)
    
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def delete_category(request,id):
    if request.user.is_superuser:
        data=category.objects.get(id=id)
        data.is_deleted=True
        data.save()
        return redirect(admin_category)
    return redirect(admin_login)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def undelete_category(request,id):
    if request.user.is_superuser:
        data=category.objects.get(id=id)
        data.is_deleted=False
        data.save()
        return redirect(admin_category)
    return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def delete_user(request,id):
    if request.user.is_superuser:
        data=customuser.objects.get(id=id)
        data.is_deleted=True
        data.save()
        return redirect(user_handling)
    return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def undelete_user(request,id):
    if request.user.is_superuser:
        data=customuser.objects.get(id=id)
        data.is_deleted=False
        data.save()
        return redirect(user_handling)
    return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)   
def user_handling(request):
    if request.user.is_superuser:
        data=customuser.objects.all()
        return render(request,'admin-user.html',{'data':data})
    return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def admin_logout(request):
    if request.user.is_superuser:
        logout(request)
        return redirect(admin_login)
    return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def user_orders(request,id):
    if request.user.is_superuser:
        user=customuser.objects.get(id=id)
        order=Order.objects.filter(user=id)
        return render(request,'adminorder.html',{'data':order,'user':user})
    return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def delivered(request,id):
    if request.user.is_superuser:
        order=Order.objects.get(id=id) 
        status = "Delivered"
        order.order_status = status
        order.save()
        return redirect(user_orders,order.user.id)
    return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def order_details(request,id):
    if request.user.is_superuser:
        order=Order.objects.get(id=id)
        items=order.items.items.all()
        return render(request,'adminorderdetails.html',{'data':items})
    return redirect(admin_login)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def sales_report(request):
    if request.method == "POST":
        start_date = request.POST.get("start-date")
        till_date = request.POST.get('end-date')
        file_format = request.POST.get('file_format')

        if start_date and till_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            till_date = datetime.strptime(till_date, '%Y-%m-%d') + timedelta(days=1)
            orders = Order.objects.filter(created_at__range=(start_date, till_date)).order_by('-created_at')
            total_sales = orders.aggregate(total_sales=Sum('total'))['total_sales']

            if file_format == 'excel':
                dataset = OrderResource().export(queryset=orders)
                response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = f'attachment; filename="sales_report_{timezone.now()}.xls"'
                return response
            elif file_format == 'pdf':
                template = 'salesreportpdf.html'
                context = {'orders': orders, 'total_sales': total_sales,'start_date':start_date,'till_date':till_date}
                pdf_data = render_to_string(template, context)
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="sales_report_{timezone.now()}.pdf"'
                pisa.CreatePDF(pdf_data, dest=response)
                return response
            else:
                # If file_format is not 'excel' or 'pdf', just render the template
                return render(request, 'salesreport.html', {'orders': orders, 'total_sales': total_sales})          
    return render(request,'salesreport.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def cat_off(request,id):
    categoryy=category.objects.get(id=id)
    if request.method == 'POST':
        percentage = float(request.POST.get('percentage'))
        datetime_str = request.POST.get('datetime')

        # Convert the datetime string to a datetime object
        valid_to = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
        if percentage<100 and percentage>0:
         categoryy.discount_percentage = percentage
         categoryy.valid_to = valid_to
         categoryy.save()
         return redirect(admin_category)
        else:
            messages.warning(request,"discount percentage cannot be greater than 100 or below 0")
    return render(request,'admin_catoff.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def delete_brand(request,id):
    brands=brand.objects.get(id=id)
    brands.is_deleted=True
    brands.save()
    return redirect(admin_brands)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def undelete_brand(request,id):
    brands=brand.objects.get(id=id)
    brands.is_deleted=False
    brands.save()
    return redirect(admin_brands)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def delete_coupons(request,id):
    coupons=coupon.objects.get(id=id)
    coupons.is_deleted=True
    coupons.save()
    return redirect(admin_coupons)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_login)
def undelete_coupons(request,id):
    coupons=coupon.objects.get(id=id)
    coupons.is_deleted=False
    coupons.save()
    return redirect(admin_coupons)







   
     
