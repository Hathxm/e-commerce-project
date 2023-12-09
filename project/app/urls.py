from django.urls import path
from app import views
# from django.conf.urls.static import static
# from django.conf import settings

urlpatterns = [
    path('', views.admin_login,name='adminlogin' ),
    path('dash',views.admin_dashboard,name='adminpg'),
    path('category',views.admin_category,name='admincategory'),
    path('reviews',views.userreviews,name='reviews'),
    path('add_category',views.add_category,name='addcategory'),
    path('add_brand',views.add_brand,name='addbrand'),
    path('add_size',views.add_size,name='addsize'),
    path('add_coupons',views.add_coupons,name='addcoupons'),
    path('brand',views.admin_brands,name='brand'),
    path('size',views.admin_size,name='size'),
    path('coupons',views.admin_coupons,name='coupons'),
    path('product',views.admin_products,name='adminproduct'),
    path('edit_product/<int:id>',views.edit_product,name='edit_product'),
    path('delete_product/<int:id>',views.delete_product,name='dlt_product'),
    path('undelete_product/<int:id>',views.undelete_product,name='undlt_product'),
    path('delete_category/<int:id>',views.delete_category,name='dlt_category'),
    path('undelete_category/<int:id>',views.undelete_category,name='undlt_category'),
    path('delete_brand/<int:id>',views.delete_brand,name='dlt_brand'),
    path('undelete_brand/<int:id>',views.undelete_brand,name='undlt_brand'),
    path('delete_user/<int:id>',views.delete_user,name='dlt_user'),
    path('undelete_user/<int:id>',views.undelete_user,name='undlt_user'),
    path('undelete_coupons/<int:id>',views.undelete_coupons,name='undlt_coupons'),
    path('delete_coupons/<int:id>',views.delete_coupons,name='dlt_coupons'),
    path('user',views.user_handling,name='userhandling'),
    path('logout',views.admin_logout,name='logout'),
    path('user_order/<int:id>',views.user_orders,name='userorders'),
    path('delivered/<int:id>',views.delivered,name='delivered'),
    path('order_details/<int:id>',views.order_details,name='orderdetails'),
    path('sales_report',views.sales_report,name='salesreport'),
    path('cat_off/<int:id>',views.cat_off,name='catoff'),
    path('dis_cat_off/<int:id>',views.dis_cat_off,name='discatoff'),


    






]