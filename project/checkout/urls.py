from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.checkout,name='checkout'),
    path('confirmation', views.confirmation,name='confirmation'),
    path('payment', views.payment_view,name='payment'),
    path('order_details',views.confirmation,name='order_details'),
    path('order_confirm',views.order_confirmed,name='order_confirm'),
    path('order_status',views.orderr_status,name='order_status'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('cancel_item/<int:id>/', views.cancel_item, name='cancel_item'),
    path('return_item/<int:id>/', views.return_item, name='return_item'),




    


]