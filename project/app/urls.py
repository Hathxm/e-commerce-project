from django.urls import path
from app import views
# from django.conf.urls.static import static
# from django.conf import settings

urlpatterns = [
    path('', views.admin_login,name='adminlogin' ),
    path('dash',views.admin_dashboard,name='adminpg'),
    path('category',views.admin_category,name='admincategory'),
    path('add_category',views.add_category,name='addcategory'),
    path('product',views.admin_products,name='adminproduct'),
    path('edit_product/<int:id>',views.edit_product,name='edit_product'),
    path('delete_product/<int:id>',views.delete_product,name='dlt_product'),
    path('undelete_product/<int:id>',views.undelete_product,name='undlt_product'),
    path('delete_category/<int:id>',views.delete_category,name='dlt_category'),
    path('undelete_category/<int:id>',views.undelete_category,name='undlt_category'),
    path('delete_user/<int:id>',views.delete_user,name='dlt_user'),
    path('undelete_user/<int:id>',views.undelete_user,name='undlt_user'),
    path('user',views.user_handling,name='userhandling'),
    path('logout',views.admin_logout,name='logout'),
    path('user_order/<int:id>',views.user_orders,name='userorders'),
    path('delivered/<int:id>',views.delivered,name='delivered'),
    










    


]