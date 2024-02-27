from rest_framework import serializers 
from .models import  Admin , Historyadmin , Categories , I3lant , OrderOut
from user.models import  User , Order , Reports
from delivery.models import Delivery
from store.models import Store
class AdminLoginSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(read_only=True)
    class Meta:
        model = Admin
        fields = ["id","is_superuser", "phone", "fullname"]  
        

class usersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","fullname", "phone" , "banned"] 

class adduserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["fullname", "phone" , "password"]          

class deliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ["id","fullname", "phone","banned" , "points" , "open" ]  

class adddeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ["fullname", "phone","password"]  

class storeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id","fullname", "phone" ,"store_name","banned" , "open" ]  

class addstoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["fullname", "phone" ,"store_name","stores_cat","storelat","storelong","password"]  

class catSerializer(serializers.ModelSerializer):
    class Meta :
        model = Categories 
        fields = '__all__'   
                 
class i3lanSerializer(serializers.ModelSerializer):
    class Meta :
        model = I3lant 
        fields = '__all__' 

class OrderSerializer(serializers.ModelSerializer):
    class Meta :
        model = Order 
        fields = ["id" ,"total", "status","created_at","user" ,"store" ,"delivery" , "items"]

class OrderOutSerializer(serializers.ModelSerializer):
    class Meta :
        model = OrderOut 
        fields = ["id" ,"total", "status","created_at","admin" ,"delivery", "user_phone" ,"user_name", ] 

class ReportSerializer(serializers.ModelSerializer):
    class Meta :
        model = Reports 
        fields = '__all__' 

class HistorySerializer(serializers.ModelSerializer):
    class Meta :
        model = Historyadmin 
        fields = '__all__' 
 
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__' 


        