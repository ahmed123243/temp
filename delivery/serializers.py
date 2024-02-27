from rest_framework import serializers 
from .models import Delivery
from user.models import Order , Reports 
from controller.models import OrderOut

#=================================auth===================================        
class authSerializer(serializers.ModelSerializer):
    class Meta :
        model = Delivery 
        fields = ["id","fullname","phone"]
        
#============================home========================
class openandpointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ["points" , "open"]

class ListOrderHomeSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.store_name')
    user_name = serializers.CharField(source='user.fullname')
    class Meta:
        model = Order
        fields = ["id", "created_at", "total", "store_name"  , "user_name", "items"]    

class ListOrderOutHomeSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='admin.fullname')
    class Meta:
        model = OrderOut
        fields = ["id","created_at", "total", "store_name" ,"user_name"]              
#============================order========================
class ListOrderSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.store_name')
    store_lat = serializers.DecimalField(source="store.storelat" , max_digits=9, decimal_places=7)
    store_long = serializers.DecimalField(source="store.storelong" , max_digits=9, decimal_places=7)
    store_phone =  serializers.CharField(source='store.phone' , max_length=10)
    user_phone =  serializers.CharField(source='user.phone', max_length=10)
    user_name = serializers.CharField(source='user.fullname')
    class Meta:
        model = Order
        fields = ["id", "status", "created_at", "total", "store_name" , "userlat" , "userlong" , "store_lat" , "store_long"  , "store_phone" , "user_phone" ,"user_name", "items"] 

class ListOrderOutSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='admin.fullname')
    store_phone =  serializers.CharField(source='admin.phone' , max_length=10)
    class Meta:
        model = OrderOut
        fields = ["id", "status", "created_at", "total", "store_name" , "store_phone" , "user_phone" ,"user_name",]     

# ===============Reports=====================
class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = ["order", "report_from", "report_to", "reason"] 


                
        