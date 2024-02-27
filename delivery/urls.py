from django.urls import path 
from . import views 

urlpatterns = [
##========================auth================================================       
   path("delivery_check", views.delivery_check),
   path("delivery_login", views.delivery_login),
   path("delivery_resetPassword", views.delivery_resetPassword),
##========================home================================================ 
   path("delivery_home/<int:pk>", views.home_delivery),    
   path("delivery_accept_order", views.order_Accept_delivery),    
   path("delivery_chnageopen", views.chnageopen),    
##========================orders================================================       
   path("delivery_orders_accepted/<int:pk>", views.orders_accepted),  
   path("delivery_orders_completed/<int:pk>", views.orders_completed),  
   path("haz_l_order", views.haz_l_order),    
   path("wasal_l_order", views.wasal_l_order), 
   path("ordercanceled", views.ordercanceled), 
   path("orderreport", views.orderreport), 
   #======================settings==============================
   path("change_pass", views.change_pass),    
]