from django.urls import path 
from . import views 

urlpatterns = [
##========================auth================================================       
    path("check_account", views.check_account),
    path("create_account", views.create_account),
    path("login", views.login),
    path("resetPassword", views.resetPassword),
##========================home================================================  
    path('home/<int:pk>',views.home),
##========================stores================================================
    path('stores/<int:pk>',views.stores),
##========================items================================================
    path('items/<int:pk>',views.items),
##========================favorite================================================
    path('fav_add_remove',views.fav_add_remove),
    path('listfav/<int:pk>',views.listfav),
##========================address_User================================================  
    path('listaddress/<int:pk>',views.listAddress),
    path('address_add_remove',views.address_add_remove),
    
##========================order_User================================================  
    path('make_order',views.make_order),
    path('list_order_user/<int:pk>',views.list_order_user),
    path('cancel_order_user/<int:pk>',views.Cancel_Order),
    path('orderreport',views.orderreport),



    path('change_pass/<int:pk>',views.change_pass),




]

