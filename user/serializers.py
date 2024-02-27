from rest_framework import serializers 
from .models import Reports, User , Address  ,Order ,Favorite
from controller.models import Categories,I3lant 
from store.models import Item, Store , Category


#================================================================userapp=======================================================================================
#=================================auth===================================
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","fullname","phone","banned"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta :
        model = User 
        fields = ["id","fullname","phone","password" ]
#=================================home===================================
class I3lantHomeSerializer(serializers.ModelSerializer):
    class Meta :
        model = I3lant
        fields = '__all__'  

class CatSerializer(serializers.ModelSerializer):
    class Meta :
        model = Categories 
        fields = '__all__'          

#=================================Stores===================================
class StoresSerializer(serializers.ModelSerializer):
    class Meta :
        model = Store 
        fields = ["id","store_name","store_logo" , "store_backgroung" , "stores_cat" ,  "open"] #"category_name_en", "category_name_ar" ,
#=================================items===================================
class ItemsSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    store_name = serializers.CharField(source='store.store_name')
    # cat_name = serializers.CharField(source='cat.name')
    open = serializers.BooleanField(source='store.open')
    class Meta :
        model = Item
        fields = [ "id", "store"    , "name","description","price" , "image"   , "active"  ,"likes", "selling" , 'store_name', "is_favorite" , "open" ]
    def get_is_favorite(self, obj):
        user_id = self.context.get('user_id')   
        try:
            Favorite.objects.get(user_id=user_id, item_id=obj.id)
            return True
        except Favorite.DoesNotExist:
            return False 

   
class categoriesSerializer(serializers.ModelSerializer):
    class Meta :
        model = Category 
        fields =  '__all__' 
        
#=================================favorite===================================
class FavoriteListSerializer(serializers.ModelSerializer):
    item = ItemsSerializer()
    class Meta:
        model = Favorite
        fields = ['item']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        item_representation = representation.pop('item')
        for key in item_representation:
            representation[key] = item_representation[key]
        return representation            

#=================================address_User===================================
class AddressSerializer(serializers.ModelSerializer):
    class Meta :
        model = Address
        fields = [ "id","name","latitude","longitude"]  

#=================================Order_User===================================
## checkout_user 
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'       
## listorder        
class ListOrderSerializer(serializers.ModelSerializer):
    delivery_phone = serializers.SerializerMethodField()
    delivery_name = serializers.SerializerMethodField()
    store_name = serializers.CharField(source='store.store_name')
    store_phone = serializers.CharField(source='store.phone')
    class Meta:
        model = Order
        fields = ["id", "status", "created_at", "items", "total", "store_name" , "store_phone", "delivery_phone", "delivery_name", "userlat" , "userlong" ]
    def get_delivery_phone(self,obj):
        phone = obj.delivery.phone if obj.delivery else "0000"
        return phone
    def get_delivery_name(self,obj):
        name = obj.delivery.fullname if obj.delivery else "null"
        return name
class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = ["order", "report_from", "report_to", "reason"]       