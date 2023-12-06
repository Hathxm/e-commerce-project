from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('<int:id>', views.checkout,name='checkout'),
    path('address', views.user_address,name='address'),
    path('payment/<int:id>', views.payment_view,name='payment'),
    path('order_details/<int:id>',views.order_details,name='order_details'),
    path('order_items/<int:id>',views.order_items,name='order_items'),
    path('wallet_payment/<int:id>',views.walletpayment,name='walletpayment'),
    path('cod/<int:id>',views.cod,name='cod'),
    path('return_order/<int:id>',views.return_order,name='return_order'),
    path('cancel_order/<int:id>',views.cancel_order,name='cancel_order'),
    path('order_status',views.orders,name='order_status'), 
    path('create_order/<int:id>',views.create_order,name='create_order'),
    path('add_to_cart/<int:id>',views.add_to_cart,name='add_to_cart'), 
    path('checkcoupon',views.checkcoupon,name='checkcoupon'), 
    path('orderinvoice/<int:id>',views.orderinvoice,name='orderinvoice'), 
  


    


   




]