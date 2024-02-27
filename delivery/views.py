
from .models import Delivery
from store.models import Item 
from controller.models import OrderOut
from user.models import Reports ,Order 
from .serializers import authSerializer,openandpointsSerializer ,ListOrderSerializer ,ReportsSerializer  , ListOrderOutSerializer , ListOrderHomeSerializer ,ListOrderOutHomeSerializer
from django.contrib.auth.hashers import check_password , make_password
from rest_framework.decorators import api_view , permission_classes,authentication_classes
from rest_framework.response import Response 
from khafofi import sendnotification , get_token
from django.db.models import Q
from rest_framework.permissions import AllowAny

# Create your views here.


##========================auth_delivery================================================    

@api_view(["POST"])
@authentication_classes([])  # Empty list means no authentication classes
@permission_classes([AllowAny])
def delivery_check(request):
    try:
        delivery = Delivery.objects.get(phone=request.data["phone"])
        if delivery.banned:
            return Response({"status": "banned"})
        else:
            return Response({"status": "exists"})
    except:    
        return Response({"status": "not existing"})




@api_view(["POST"])
@authentication_classes([])  # Empty list means no authentication classes
@permission_classes([AllowAny])
def delivery_login(request):
    try:
        delivery = Delivery.objects.get(phone=request.data["phone"])
        is_password_correct = check_password(request.data['password'], delivery.password) 
        if is_password_correct :
            if delivery.banned :
                return Response({"status": "banned"})
            else :
                serializer = authSerializer(delivery)
                return Response({"status": "success" , 'delivery' : serializer.data , "token" : get_token.getToke()})    
        else: 
            return Response({"status": "wrong password"})
    except :
        return Response({"status": "not existing"})


@api_view(["POST"])
@authentication_classes([])  # Empty list means no authentication classes
@permission_classes([AllowAny])
def delivery_resetPassword(request):
    try:
        delivery = Delivery.objects.get(phone=request.data["phone"])
        delivery.password =  make_password(request.data['password'])
        delivery.save()
        serializer = authSerializer(delivery)
        return Response({"status": "success",'delivery' : serializer.data , "token" : get_token.getToke()})
    except :
        return Response({"status": "failure"})



##========================home================================================

@api_view(['GET'])
def home_delivery(request , pk):
    try :
        delivery=  Delivery.objects.get(id=pk)
        if delivery.banned :
                return Response({"status": "banned"}) 
        else :
            serializeropenandpoints = openandpointsSerializer(delivery)
            if delivery.open :
                orders_out = OrderOut.objects.filter(status=2)
                serializer_out = ListOrderOutHomeSerializer(orders_out , many = True)
                order = Order.objects.filter(status=2)
                serializerOrders = ListOrderHomeSerializer(order , many = True)
                return Response({"status": "success","openandpoints" : serializeropenandpoints.data ,"orders": serializerOrders.data + serializer_out.data}) 
            else:      
                return Response({"status": "success","openandpoints" : serializeropenandpoints.data ,"orders": []})  
    except :
        return Response({"status": "failure"})
    

@api_view(['POST'])
def chnageopen(request):
    try :
        delivery=  Delivery.objects.get(id=request.data["delivery_id"])
        if delivery.points == 0 and request.data["open"]  :
            return Response({"status": "5alas"  })
        else :
            delivery.open = request.data["open"]
            delivery.save()
            serializeropenandpoints = openandpointsSerializer(delivery)
            return Response({"status": "success" , "openandpoints" : serializeropenandpoints.data, })
    except :
        return Response({"status": "failure"})
    
@api_view(['POST'])
def order_Accept_delivery(request):
    try:
        try :   
            if  request.data["is_out"]:
                order = OrderOut.objects.get(id=request.data["order_id"] ,status=2)   
            else :
                order = Order.objects.get(id=request.data["order_id"] ,status=2)
        except Order.DoesNotExist :
            return Response({"status": "not existing"})
        delivery = Delivery.objects.get(id =request.data["delivery_id"])
        if delivery.points == 0  :
            return Response({"status": "5alas"})
        order.status = 3 
        order.delivery = delivery
        order.save()
        delivery.subtract_points(amount=1)
        if  request.data["is_out"]  :
            sendnotification.send_notification("تمت الموافقة على الطلب" ,f"عامل التوصيل  على الطريق" ,f"admin{order.admin.id}" , "/" , "") 
        else :
            sendnotification.send_notification("تمت الموافقة على الطلب" ,f"عامل التوصيل  على الطريق" ,f"store{order.store.id}" , "/orderlist" , "refreshaccepted")
        return Response({"status": "success"})
    except :
        return Response({"status": "failure"})    

##========================order================================================
@api_view(['POST'])
def ordercanceled(request ):
    try :
        if  request.data["is_out"]:
            order = OrderOut.objects.get(id=request.data["order_id"] ,status=3)   
        else :
            order = Order.objects.get(id=request.data["order_id"] ,status=3)   
        delivery =  Delivery.objects.get(id=order.delivery.id ,)
        order.status =  2
        order.delivery = None
        order.save()
        delivery.add_points(amount=1)
        sendnotification.send_notification("توجد طلبية " ,"سارع في قبول الطلبية" ,"delivery" , "/orderlist" , "RefreshHome")
        sendnotification.send_notification("تم الإلغاء" ,f"جاري البحث عن عامل توصيل ثاني" ,f"store{order.store.id}" , "/orderlist" , "refreshaccepted")
        return Response({"status": "success",})        
    except :
        return Response({"status": "failure"})  
    
@api_view(['GET'])
def orders_accepted(request , pk):
    try :   
        order = Order.objects.filter(Q(status=3, delivery=pk)  | Q(status=4, delivery=pk))
        serializerOrders = ListOrderSerializer(order , many = True)
        orders_out = OrderOut.objects.filter(Q(status=3, delivery=pk)  | Q(status=4, delivery=pk))
        serializer_out = ListOrderOutSerializer(orders_out , many = True)
        return Response({"status": "success","orders": serializerOrders.data + serializer_out.data})        
    except :
        return Response({"status": "failure"}) 
     
@api_view(['GET'])
def orders_completed(request , pk):
    try :   
        order = Order.objects.filter(status=5, delivery=pk)
        serializerOrders = ListOrderSerializer(order , many = True)
        order_out = OrderOut.objects.filter(status=5, delivery=pk)
        serializerOrdersout = ListOrderOutSerializer(order_out , many = True)
        return Response({"status": "success","orders": serializerOrders.data + serializerOrdersout.data})        
    except :
        return Response({"status": "failure"})        


    
@api_view(['POST'])
def haz_l_order(request):
    try:
        if  request.data["is_out"]:
            order = OrderOut.objects.get(id=request.data["order_id"] ,status=3)   
        else :
            order = Order.objects.get(id=request.data["order_id"] ,status=3)
            sendnotification.send_notification("تم تجهيز الطلبية" ,f"الطلبية على الطريق" ,f"user{order.user.id}" , "/orderlist" , "RefreshOrder")
        order.status = 4 
        order.save()
        return Response({"status": "success"})
    except :
        return Response({"status": "failure"})


@api_view(['POST'])
def wasal_l_order(request):
    try:
        if  request.data["is_out"]:
            order = OrderOut.objects.get(id=request.data["order_id"] ,status=4)
        else :    
            order = Order.objects.get(id=request.data["order_id"] ,status=4)
            sendnotification.send_notification("تم توصيل الطلبية" ,f" ♥♥ نشكركم  " ,f"user{order.user.id}" , "/orderlist" , "RefreshOrder")
            sendnotification.send_notification("تم توصيل الطلبية" ,f"بنجاح {order.id} تم توصيل الطلبية رقم" ,f"store{order.store.id}" , "" , "")
            for item in order.items:
                items = Item.objects.get(id=item["id"])
                items.add_sell()
        order.status = 5
        order.save()    
        return Response({"status": "success"})
    except :
        return Response({"status": "failure"})
    
@api_view(['POST'])
def orderreport(request) :
    try:
        reportExi = Reports.objects.filter(order=request.data['order'],report_from=request.data['report_from'],report_to=request.data['report_to']).exists()
        if reportExi :
            return Response({"status": "exists"})
        serializer = ReportsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            sendnotification.send_notification("يوجد إبلاغ" ,f"من قبل عامل التوصيل" ,f"admin" , "" , "")
            return Response({"status": "success"})
        else :
            return Response({"status": "failure"}) 
    except :
        return Response({"status": "failure"})



# ============================settings==========
@api_view(["POST"])
def change_pass(request):
    try:
        delivery = Delivery.objects.get(id=request.data['delivery_id'])
        is_oldpassword_correct = check_password(request.data['oldpass'], delivery.password) 
        if is_oldpassword_correct:
            delivery.password = make_password(request.data['newpass'])
            delivery.save()
            return Response({"status": "success"})
        else :
            return Response({"status": "wrong password"})
    except :
        return Response({"status": "failure"})
    




  