from django.urls import path 
from .views import  login ,list_add_delete_admin,list_add_ban_user,list_add_ban_delivery,addPoints_delivery,list_add_ban_store , list_add_cat, edit_delete_cat , list_add_i3lan , edit_delete_i3lan , list_add_order , delete_order , delete_old_orders , list_report , send_noti , history  , change_pass 

urlpatterns = [
       #==========================admin=========================
   path("login", login),   
   path("list_add_delete_admin", list_add_delete_admin),
   path("change_pass", change_pass),
   
   path("list_add_ban_user", list_add_ban_user),

   path("list_add_ban_delivery", list_add_ban_delivery),
   path("addPoints_delivery/<int:pk>", addPoints_delivery),
 
   path("list_add_ban_store", list_add_ban_store),

   path("list_add_cat", list_add_cat),
   path("edit_delete_cat", edit_delete_cat),
   
   path("list_add_i3lan", list_add_i3lan),
   path("edit_delete_i3lan", edit_delete_i3lan),

   path("list_add_order", list_add_order),
   path("delete_order", delete_order),
   path("delete_old_orders", delete_old_orders),

   path("list_report", list_report),

   path("send_noti", send_noti),

   path("history", history),



]