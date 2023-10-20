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
from user.models import cart
from django.db.models import Sum
from user.views import user_login

# Create your views here.
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required(login_url=user_login)
# def checkout(request):
#      user=request.user
#      carts=cart.objects.get(user=user)
#      data=cart.items.all()
#      return render(request,'checkout.html',{'data':data})