from user.models import Order , Reports
from controller.models import Categories
from .models import Category , Store , Item

from rest_framework.response import Response 
from rest_framework.decorators import api_view , permission_classes,authentication_classes
from delivery.serializers import ReportsSerializer
from khafofi import sendnotification , get_token
from .serializers import AuthSerializer ,ListOrderHomeSerializer ,ListCatSerializer ,AddCatSerializer,EditCatSerializer,AddItemSerializer,EditItemSerializer ,ItemsSerializer ,ListOrderAcceptedSerializer ,StoreSerializer,catSerializer
from django.contrib.auth.hashers import check_password , make_password
from django.db.models import Q
from django.conf import settings
import os
from datetime import datetime
from rest_framework.permissions import AllowAny



# Create your views here.


##========================auth_store================================================    

@api_view(["POST"])
@authentication_classes([])  # Empty list means no authentication classes
@permission_classes([AllowAny])
def check_account(request):
    try:
        store= Store.objects.get(phone=request.data["phone"])
        if store.banned == True:
            return Response({"status": "banned"}) 
        else:
            return Response({"status": "exists"})
    except:    
        return Response({"status": "not existing"})




@api_view(["POST"])
@authentication_classes([])  # Empty list means no authentication classes
@permission_classes([AllowAny])
def login(request):
    try:
        store = Store.objects.get(phone=request.data["phone"])
        is_password_correct = check_password(request.data['password'], store.password) 
        if is_password_correct :
            if store.banned :
                return Response({"status": "banned"})
            else:
                serializer = AuthSerializer(store)
                return Response({"status": "success" , 'store' : serializer.data , "token" : get_token.getToke()})    
        else: 
            return Response({"status": "wrong password"})
    except :
        return Response({"status": "not existing"})


@api_view(["POST"])
@authentication_classes([])  # Empty list means no authentication classes
@permission_classes([AllowAny])
def resetPassword(request):
    try:
        store = Store.objects.get(phone=request.data["phone"])
        store.password = make_password(request.data['password']) 
        store.save()
        serializer = AuthSerializer(store)
        return Response({"status": "success" , 'store' : serializer.data ,  "token" : get_token.getToke()})
    except :
        return Response({"status": "failure"})
    
    
    
    
#=================================home==================================
@api_view(['GET'])
def home(request , pk):
    try :
        store=  Store.objects.get(id=pk) 
        if store.banned == True :
            return Response({"status": "banned"})
        else :
            if store.open :
                order = Order.objects.filter(status=0 , store=pk)
                serializerOrders = ListOrderHomeSerializer(order , many = True)
                response_data = {
                            "status": "success",
                            "open" : store.open ,
                            "orders": serializerOrders.data
                }
                return Response(response_data)    
            else:    
                return Response({"status": "success","open" : store.open ,"orders": []})  
    except :
        return Response({"status": "failure"}) 
    
    
@api_view(['POST'])
def chnageopen(request):
    try :
        store=  Store.objects.get(id=request.data["store_id"])
        store.open = request.data["open"]
        store.save()
        return Response({"status": "success" , "open" : store.open, })
    except :
        return Response({"status": "failure"})    
    
    
@api_view(['POST'])
def accept_order(request):
    try:
        order = Order.objects.get(id=request.data["order_id"] ,status=0)   
        order.status = 1 
        order.save()
        sendnotification.send_notification("تمت الموافقة على الطلبية" ,"يتم تجهيز طلبك" ,f"user{order.user.id}" , "/orderlist" , "RefreshOrder")
        return Response({"status": "success" })
    except :
        return Response({"status": "failure"})
    
    
#=================================categories===================================
@api_view(['GET' , 'DELETE'])
def list_delete_category(request , pk):
    try :   
        if request.method == 'GET':
            category = Category.objects.filter(store=pk)
            serializercategory = ListCatSerializer(category , many = True)
            categories = serializercategory.data
            return Response({"status": "success","categories": categories})  
        elif request.method == 'DELETE':  
            category = Category.objects.get(id=pk)  
            if category.count == 0 :
                category.delete()
                return Response({
                 "status": "success",
                })
            else :
                return Response({
                 "status": "delete_items",
                })
    except :
        return Response({"status": "failure"})  
    
@api_view(['POST' , "PUT"])
def add_edit_category(request):
    try :  
        if request.method == "POST": 
            serializer = AddCatSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success",})
            else :
                return Response({"status": "failure" ,  "msg" : serializer.errors})
        elif request.method == "PUT":  
            category = Category.objects.get(id=request.data['cat'])
            serializer = EditCatSerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success"} )
            else:
                return Response({"status": "failure" , "msg" : serializer.errors})           
    except Exception as e: 
        return Response({"status": "failure" , "msg" : str(e)}) 

#=================================items===================================     

@api_view(["GET" , 'DELETE'])
def list_delete_item(request , pk ):
    try:
        if request.method == 'GET':    
            items = Item.objects.filter(store=pk)
            categories = Category.objects.filter(store=pk,)
            serialized_categories = []
            for category in categories:
                category_data = ListCatSerializer(category).data
                category_items = items.filter(cat=category.id)
                category_data["items"] = ItemsSerializer(category_items, many=True).data
                serialized_categories.append(category_data)
            return Response({"status": "success","category": serialized_categories})  
        elif request.method == 'DELETE':
            item = Item.objects.get(id=pk)
            image_path = os.path.join(settings.MEDIA_ROOT, str(item.image))
            item.cat.remove_item() 
            item.delete()
            if os.path.exists(image_path):
                os.remove(image_path)
            return Response({"status": "success",}) 
    except :  
        return Response({"status": "failure"}) 
        
@api_view(['POST' , "PUT"])
def add_edit_item(request):
    try :   
        if request.method == "POST": 
            store_id = request.data['store']
            cat = request.data['cat']
            category = Category.objects.get(id=cat)
            ext = request.data["image"].name.split('.')[-1]
            timenow = datetime.now().strftime("%Y%m%d%H%M%S")
            new_filename = f'store{store_id}_item_{timenow}.{ext}'
            request.data["image"].name = new_filename
            serializer = AddItemSerializer(data=request.data ,)
            if serializer.is_valid():
                serializer.save()
                category.add_item()
                return Response({"status": "success",})
            else :
                return Response({"status": "failure" , "msg":serializer.errors}) 
        elif request.method == 'PUT':   
            item = Item.objects.get(id=request.data['itemId'])
            image_path = os.path.join(settings.MEDIA_ROOT, str(item.image))
            if 'image' in request.data:
                ext = request.data["image"].name.split('.')[-1]
                timenow = datetime.now().strftime("%Y%m%d%H%M%S")
                new_filename = f'store{item.store.id}_item_{timenow}.{ext}'
                request.data["image"].name = new_filename
            serializer = EditItemSerializer(item, data=request.data,)
            if serializer.is_valid():
                if os.path.exists(image_path) and 'image' in request.data:
                    os.remove(image_path)
                category = Category.objects.get(id=request.data['cat'])
                if item.cat.id !=   category.id :
                    item.cat.remove_item()
                    category.add_item()
                serializer.save()
                return Response({"status": "success"} )
            else :
                return Response({"status": "failure" , "msg" : serializer.errors})     
    except Exception as e:
        return Response({"status": "failure" , "msg":str(e) })
        

#=================================Order===================================

@api_view(['GET'])
def orders_accepted(request , pk):
    try :   
        order = Order.objects.filter(store=pk).exclude(Q(status=5) | Q(status=0))
        serializerOrders = ListOrderAcceptedSerializer(order , many = True)
        return Response({"status": "success","orders": serializerOrders.data})        
    except :
        return Response({"status": "failure"})  
    
    
@api_view(['POST'])
def finish_order(request):
    try:
        order = Order.objects.get(id=request.data["order_id"] ,status=1)
        sendnotification.send_notification("توجد طلبية " ,"سارع في قبول الطلبية" ,"delivery" , "/orderlist" , "RefreshHome")
        order.status = 2 
        order.save()
        return Response({"status": "success" })
    except :
        return Response({"status": "failure" })
    
@api_view(['POST'])
def orderreport(request) :
    reportExi = Reports.objects.filter(order=request.data['order'],report_from=request.data['report_from'],report_to=request.data['report_to']).exists()
    if reportExi :
        return Response({"status": "exists"})
    serializer = ReportsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        sendnotification.send_notification("يوجد إبلاغ" ,f"من قبل المتجر" ,f"admin" , "" , "")
        return Response({"status": "success"})
    else :
        return Response({"status": "failure"}) 
    
@api_view(['GET'])
def orders_completed(request , pk):
    try :   
        order = Order.objects.filter(Q(status=5, store=pk))
        serializerOrders = ListOrderAcceptedSerializer(order , many = True)
        return Response({"status": "success","orders": serializerOrders.data})        
    except Exception :
        return Response({"status": "failure"})      
    




#=================================settings===================================    
@api_view(['Get' , "PUT"])
def get_edit_info(request,pk ):
    try:
        store = Store.objects.get(id=pk)
        if request.method == 'GET':    
            serializerstore = StoreSerializer(store)
            cat = Categories.objects.all()
            Serializercat = catSerializer(cat, many=True)
            return Response({"status": "success" , "store" : serializerstore.data , "cat" : Serializercat.data})  
        elif request.method == 'PUT': 
            logo_path = os.path.join(settings.MEDIA_ROOT, str(store.store_logo))
            backgroung_path = os.path.join(settings.MEDIA_ROOT, str(store.store_backgroung))
            if 'store_logo' in request.data:
                ext = request.data["store_logo"].name.split('.')[-1]
                timenow = datetime.now().strftime("%Y%m%d%H%M%S")
                new_filename = f'storelogo{pk}_{timenow}.{ext}'
                request.data["store_logo"].name = new_filename
            if 'store_backgroung' in request.data:
                ext = request.data["store_backgroung"].name.split('.')[-1]
                timenow = datetime.now().strftime("%Y%m%d%H%M%S")
                new_filename = f'store_backgroung{pk}_{timenow}.{ext}'
                request.data["store_backgroung"].name = new_filename    
            serializer = StoreSerializer(store, data=request.data)
            if serializer.is_valid():
                if os.path.exists(logo_path) and 'store_logo' in request.data and str(store.store_logo) != "stores_logo/default_logo.png":
                    os.remove(logo_path) 
                if os.path.exists(backgroung_path) and 'store_backgroung' in request.data and str(store.store_backgroung) != "stores_background/default_background.jpg":
                    os.remove(backgroung_path)    
                serializer.save()
                return Response({"status": "success"} )
            else:
                return Response({"status": "failure" , "msg" : serializer.errors})   
    except :
        return Response({"status": "failure"})

@api_view(["POST"])
def change_pass(request,pk):
    try:
        store = Store.objects.get(id=pk)
        is_oldpassword_correct = check_password(request.data['oldpass'], store.password) 
        if is_oldpassword_correct:
            store.password = make_password(request.data['newpass'])
            store.save()
            return Response({"status": "success"})
        else :
            return Response({"status": "wrong password"})
    except :
        return Response({"status": "failure"})



