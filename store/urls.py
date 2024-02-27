from django.urls import path 
from . import views 


urlpatterns = [
##========================auth================================================       
    path("check_account", views.check_account),
    path("login", views.login),
    path("resetPassword", views.resetPassword),
##========================home================================================   
    path('home/<int:pk>',views.home),
    path('accept_order',views.accept_order),
    path('chnageopen',views.chnageopen),
##========================categories================================================   
   path('list_delete_category/<int:pk>',views.list_delete_category),
   path('add_edit_category',views.add_edit_category),
   ##========================items================================================   
   path('list_delete_item/<int:pk>',views.list_delete_item),
   path('add_edit_item',views.add_edit_item),
##========================order================================================   
    path("orders_accepted/<int:pk>", views.orders_accepted),  
    path('finish_order',views.finish_order),
    path("order_report", views.orderreport), 
    path("orders_completed/<int:pk>", views.orders_completed),  
#======================settings==============================
    path("get_edit_info/<int:pk>", views.get_edit_info), 
    path("change_pass/<int:pk>", views.change_pass), 
]