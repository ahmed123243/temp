import os
from rest_framework.decorators import api_view , permission_classes,authentication_classes
from rest_framework.response import Response 
from .models import Admin , Historyadmin , Categories , I3lant , OrderOut
from django.contrib.auth.hashers import check_password , make_password
from user.models import User , Order , Reports
from store.models import Store 
from delivery.models import Delivery
from .serializers import AdminSerializer ,AdminLoginSerializer , usersSerializer , deliverySerializer ,adddeliverySerializer,storeSerializer , catSerializer ,addstoreSerializer , i3lanSerializer , OrderSerializer , ReportSerializer , HistorySerializer , OrderOutSerializer , adduserSerializer
from khafofi import sendnotification, settings
from datetime import datetime , timedelta , timezone
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
@api_view(["POST"])
@authentication_classes([])  # Empty list means no authentication classes
@permission_classes([AllowAny])
def login(request):
    try:
        admin = Admin.objects.get(phone=request.data["phone"])
        is_password_correct = check_password(request.data['password'], admin.password) 
        if is_password_correct:
            serializer = AdminLoginSerializer(admin,data=request.data)
            if serializer.is_valid():
                token = Token.objects.get(user=admin)
                return Response({"status": "success" , 'admin' : serializer.data , "token" : token.key})
            else :
                return Response({"status": "failure" ,  "err" : serializer.errors})    
        else :
            return Response({"status": "failure" ,  "err" : "password uncorrect"})  
    except Exception as e:  
        return Response({"status": "failure" ,  "err" : str(e) })    
          
@api_view(["GET" , 'PUT' , 'POST'])
def list_add_ban_user(request):
    try:
        if request.method == "GET":
            users = User.objects.all()
            serializer = usersSerializer(users , many = True)
            return Response({"status": "success", "users": serializer.data})  
        elif request.method == 'POST': 
            request.data["password"] = make_password(request.data["password"])
            serializer = adduserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success",})
            else :
                return Response({"status": "failure" ,  "err" : serializer.errors}) 
        else:
            user_id = request.data["user_id"]
            user = User.objects.get(pk=user_id)
            user.banned = request.data["ban"]
            user.save()
            return Response({"status": "success"})  
    except Exception as e: 
        return Response({"status": "failure" , "err" : str(e) }) 
    
@api_view(["GET","POST" , "PUT"])
def list_add_ban_delivery(request):
    try:
        if request.method == "GET":
            deliverys = Delivery.objects.all()
            serializer = deliverySerializer(deliverys , many = True)
            return Response({"status": "success", "deliverys": serializer.data})
        elif request.method == 'POST': 
            request.data["password"] = make_password(request.data["password"])
            serializer = adddeliverySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success",})
            else :
                return Response({"status": "failure" ,  "err" : serializer.errors}) 
        elif request.method == 'PUT':
            deliveryid = request.data["delivery_id"] 
            delivery = Delivery.objects.get(pk=deliveryid)
            delivery.banned =  request.data["ban"]
            delivery.open = False
            delivery.save()
            return Response({"status": "success"})  
    except Exception as e: 
        print(str(e))
        return Response({"status": "failure" , "err" : str(e) }) 
    
@api_view(["POST"])
def addPoints_delivery(request,pk):
    try:
        points = request.data["points"]
        deliveryid = request.data["delivery_id"]
        delivery = Delivery.objects.get(pk=deliveryid)
        delivery.add_points(amount=points)
        sendnotification.send_notification("تم تعبئة نقاطك" ,f"{points} نقطة" ,f"delivery{deliveryid}" , "" , "")
        Historyadmin.objects.create(admin=Admin.objects.get(pk=pk),reason= f"إضافة {points} نقاط لعامل التوصيل #{deliveryid}").save()
        return Response({"status": "success"})
    except Exception as e:  
        return Response({"status": "failure" , "err" : str(e) })    

@api_view(["GET", 'POST' , 'PUT'])
def list_add_ban_store(request):
    try:
        if request.method == "GET":
            stores = Store.objects.all()
            serializerstore = storeSerializer(stores , many = True)
            cat = Categories.objects.all()
            Serializercat = catSerializer(cat, many=True)
            return Response({"status": "success", "stores": serializerstore.data , "categories" : Serializercat.data})  
        elif request.method == 'POST':  
            request.data["password"] = make_password(request.data["password"])
            serializer = addstoreSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response( {"status": "success",})
            else :
                return Response({"status": "failure" , "err" : serializer.errors })
        elif request.method == 'PUT':     
            store = Store.objects.get(pk=request.data["store_id"])
            store.banned = request.data["ban"]
            store.open = False
            store.save()
            return Response({"status": "success"})     
    except Exception as e:  
        return Response({"status": "failure" , "err" : str(e) }) 

@api_view(["GET" , 'POST'])
def list_add_cat(request):
    try:
        if request.method == "GET":
            cat = Categories.objects.all()
            Serializercat = catSerializer(cat, many=True)
            return Response({"status": "success", "categories" : Serializercat.data})
        elif request.method == 'POST':  
            catName = request.data['category_name_en']
            ext = request.data["image"].name.split('.')[-1]
            timenow = datetime.now().strftime("%Y%m%d%H%M%S")
            new_filename = f'{catName}_{timenow}.{ext}'
            request.data["image"].name = new_filename
            serializer = catSerializer(data=request.data,)
            if serializer.is_valid():
                serializer.save()
                return Response({
                "status": "success",
                })
            else:
                return Response({"status": "failure" , "err" : serializer.errors})     
    except Exception as e:  
        return Response({"status": "failure" , "err" : str(e) }) 

@api_view(["PUT", 'DELETE'])
def  edit_delete_cat(request):
    try :
        cat = Categories.objects.get(id=request.data['cat_id'])
        image_path = os.path.join(settings.MEDIA_ROOT, str(cat.image))
        if request.method == "PUT":
            if 'image' in request.data:
                catName = request.data['category_name_en']
                ext = request.data["image"].name.split('.')[-1]
                timenow = datetime.now().strftime("%Y%m%d%H%M%S")
                new_filename = f'{catName}_{timenow}.{ext}'
                request.data["image"].name = new_filename
            serializer = catSerializer(cat, data=request.data,)
            if serializer.is_valid():
                if os.path.exists(image_path) and 'image' in request.data:
                    os.remove(image_path)
                serializer.save()
                return Response({"status": "success"} )
            else :
                return Response({"status": "failure" , "err" : serializer.errors})
        elif request.method == 'DELETE':
            cat.delete()
            if os.path.exists(image_path):
                os.remove(image_path)
            return Response({
            "status": "success",
            })
    except Exception as e:
        return Response({"status": "failure" ,  "err" : str(e) }) 
    
@api_view(['POST',"GET"])
def list_add_i3lan(request):
    try :   
        if request.method == "POST":
            ext = request.data["image"].name.split('.')[-1]
            timenow = datetime.now().strftime("%Y%m%d%H%M%S")
            new_filename = f'i3lan_{timenow}.{ext}'
            request.data["image"].name = new_filename
            serializer = i3lanSerializer(data=request.data,)
            if serializer.is_valid():
                serializer.save()
                return Response({
                "status": "success",
                })
            else:
                return Response({"status": "failure" , "err" : serializer.errors})  
        else :
            i3lant = I3lant.objects.all()
            serializer = i3lanSerializer(i3lant , many = True)
            return Response({"status": "success", "i3lant": serializer.data })  
    except Exception as e:
        return Response({"status": "failure" , "err" : str(e) })
    
@api_view(["PUT", 'DELETE'])
def edit_delete_i3lan(request):
    try :
        i3lan = I3lant.objects.get(id=request.data["i3lan_id"])
        image_path = os.path.join(settings.MEDIA_ROOT, str(i3lan.image))
        if request.method == "PUT":
            if 'image' in request.data:
                ext = request.data["image"].name.split('.')[-1]
                timenow = datetime.now().strftime("%Y%m%d%H%M%S")
                new_filename = f'i3lan_{timenow}.{ext}'
                request.data["image"].name = new_filename
            serializer = i3lanSerializer(i3lan, data=request.data,)
            if serializer.is_valid():
                if os.path.exists(image_path) and 'image' in request.data:
                    os.remove(image_path)
                serializer.save()
                return Response({"status": "success"} )
            else :
                return Response({"status": "failure" , "err" : serializer.errors})
        elif request.method == 'DELETE':
            i3lan.delete()
            if os.path.exists(image_path):
                os.remove(image_path)
            return Response({
            "status": "success",
            })
    except Exception as e:
        return Response({"status": "failure" ,  "err" : str(e) }) 

@api_view(["GET" , "POST"])
def list_add_order(request):
    try :
        if request.method == "GET" :
            orders = Order.objects.all()
            serializer = OrderSerializer(orders , many = True)
            orders_out = OrderOut.objects.all()
            serializer_out = OrderOutSerializer(orders_out , many = True)
            return Response({"status": "success", "orders": serializer.data  + serializer_out.data}) 
        elif request.method == "POST":
            serializer = OrderOutSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                sendnotification.send_notification("توجد طلبية " ,"سارع في قبول الطلبية" ,"delivery" , "/orderlist" , "RefreshHome")
                return Response( {
                "status": "success",
                })
    except Exception as e:
        return Response({"status": "failure" , "err" : str(e) })
    
@api_view(["DELETE"])
def delete_order(request):
    try:
        if  request.data["is_out"]:
            order = OrderOut.objects.get(id=request.data["order_id"])   
        else :
            order = Order.objects.get(id=request.data["order_id"])      
        order.delete()
        return Response({"status": "success"})  
    except Exception as e:
        return Response({"status": "failure" , "err" : str(e) })
    
@api_view(["DELETE"])
def delete_old_orders(request):
    try:   
        current_time = datetime.now(timezone.utc)
        threshold_date = current_time - timedelta(days=30)
        old_orders = Order.objects.filter(created_at__lt=threshold_date)
        for order in old_orders:
            order.delete()  
        old_orders_out = OrderOut.objects.filter(created_at__lt=threshold_date)
        for order in old_orders_out:
            order.delete()      
        return Response({"status": "success"})  
    except Exception as e:
        return Response({"status": "failure" , "err" : str(e) })

@api_view(["GET"])
def list_report(request):
    try :   
        reports = Reports.objects.all()
        serializer = ReportSerializer(reports , many = True)
        return Response({"status": "success", "reports": serializer.data })  
    except Exception as e:
        return Response({"status": "failure" , "err" : str(e) })
    
@api_view(["POST"])
def send_noti(request):
    try : 
        type = request.data["type"]
        who = request.data["who"]
        title = request.data["title"]
        msg = request.data["msg"]
        sendnotification.send_notification(f"{title}" ,f"{msg}",f"{type}{who}", "" , "")    
        return Response({"status": "success"})  
    except Exception as e:
        return Response({"status": "failure" , "err" : str(e) })   

@api_view(["GET"])
def history(request):
    try : 
        history = Historyadmin.objects.all() 
        serializer = HistorySerializer(history , many = True)
        return Response({"status": "success" , "history": serializer.data})  
    except Exception as e:
        print(e)
        return Response({"status": "failure" , "err" : str(e) })
    

@api_view(["POST" , 'DELETE' , "GET"])
def list_add_delete_admin(request):
    try:
        if request.method == "POST" :
            request.data["password"] = make_password(request.data["password"])
            serializer = AdminSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()       
                return Response( {
                "status": "success",
                })
            else :
                return Response({"status": "failure" ,  "err" : serializer.errors})  
        elif request.method == 'DELETE':
            admin_id =  request.data['admin_id']
            admin = Admin.objects.get(id=admin_id)
            if admin.id == 1 :
                return Response({"status": "failure"}) 
            admin.delete()
            return Response({"status": "success"}) 
        else:
            admins = Admin.objects.all()
            serializer = AdminLoginSerializer(admins , many = True)
            return Response({"status": "success", "admins": serializer.data })  
    except Exception as e:
        return Response({"status": "failure" , "err" : str(e) })      
    
@api_view(["POST"])
def change_pass(request):
    try:
        admin = Admin.objects.get(id=request.data['admin_id'])
        is_oldpassword_correct = check_password(request.data['oldpass'], admin.password) 
        if is_oldpassword_correct:
            admin.password = make_password(request.data['newpass'])
            admin.save()
            return Response({"status": "success"})
        else :
            return Response({"status": "wrong password"})
    except Exception as e :
        return Response({"status": "failure"  , "err" : str(e) })    