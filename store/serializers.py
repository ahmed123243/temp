from rest_framework import serializers 
from .models import Store , Category , Item
from user.models import Order , Reports
from controller.models import Categories
#=================================auth===================================

class AuthSerializer(serializers.ModelSerializer):
    class Meta :
        model = Store 
        fields = ["id","fullname","phone"]
        
#=================================categories===================================    
class ListCatSerializer(serializers.ModelSerializer):
    class Meta :
        model = Category 
        fields = '__all__' 

class AddCatSerializer(serializers.ModelSerializer):
    class Meta :
        model = Category 
        fields = ["id","name","store"]   

class EditCatSerializer(serializers.ModelSerializer):
    class Meta :
        model = Category 
        fields = ["id","name"]                

#=================================items===================================    
class ItemsSerializer(serializers.ModelSerializer):
    class Meta :
        model = Item 
        fields = [ "id", "store", "cat"  , "name","description","price" , "image"  , "active"  ,"likes", "selling" ]
   
class AddItemSerializer(serializers.ModelSerializer):
    class Meta :
        model = Item
        fields = [ "store"  , "cat"  , "name","description","price" , "image"  , "active" ] 

class EditItemSerializer(serializers.ModelSerializer):
    class Meta :
        model = Item
        fields = [  "cat"  , "name","description","price" , "image"   , "active"  ]         
        
#============================order==============================================
class ListOrderHomeSerializer(serializers.ModelSerializer):
    user_phone =  serializers.CharField(source='user.phone', max_length=10)
    user_name =  serializers.CharField(source='user.fullname' , max_length=25)
    class Meta :
        model = Order 
        fields = ["id", "created_at", "items", "total"  , "user_phone" ,"user_name" ] 
         
class ListOrderAcceptedSerializer(serializers.ModelSerializer):
    user_phone =  serializers.CharField(source='user.phone', max_length=10)
    user_name =  serializers.CharField(source='user.fullname' , max_length=25)
    delivery_phone =  serializers.SerializerMethodField()
    delivery_name =  serializers.SerializerMethodField()
    class Meta :
        model = Order 
        fields = ["id", "status", "created_at", "items", "total"  , "user_phone" ,"user_name" , "delivery_phone" ,"delivery_name"]
    def get_delivery_phone(self,obj):
        phone = obj.delivery.phone if obj.delivery else "0000"
        return phone
    def get_delivery_name(self,obj):
        name = obj.delivery.fullname if obj.delivery else "null"
        return name

class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = ["id", "order", "report_from", "report_to", "reason"] 
                          
#============================store_info==============================================          
class StoreSerializer(serializers.ModelSerializer):
    class Meta :
        model = Store 
        fields = ["store_name","store_logo","store_backgroung"  , "storelat" , "storelong"  , "stores_cat"]
        
class catSerializer(serializers.ModelSerializer):
    class Meta :
        model = Categories 
        fields = ["id" , "category_name_ar"]
        
      

        
        
        