from django.urls import path
from user import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.landing_page,name='landing-pg' ),
    path('contact',views.contact,name='contact'),
    path('signup',views.user_signup,name='usersignup'),
    path('details/<int:id>',views.details,name='details'),
    path('login',views.user_login,name='userlogin'),
    path('forgotpass',views.forgot_password,name='forgotpass'),
    path('otp',views.verify_otp,name='otp'),
    path('shop',views.shop,name='shop'),
    path('profile',views.user_profile,name='userprofile'),
    path('logout',views.user_logout,name='userlogout'),
    path('women',views.womens,name='women'),
    path('men',views.mens,name='men'),
    path('accessories',views.accessories,name='accessories'),
    path('product_details/<int:id>',views.product_details,name='product_details'),
    path('viewcart',views.viewcart,name='viewcart'),
    path('dltfrmordr<int:id>',views.delete_from_orders,name='dltfrmordr'),

    








]
urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

