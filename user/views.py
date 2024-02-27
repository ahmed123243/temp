
from rest_framework.decorators import api_view , permission_classes,authentication_classes
from rest_framework.response import Response 
from .models import Reports, User   , Favorite , Address, Order
from store.models import Item, Store , Category
from delivery.models import Delivery
from controller.models import Categories , I3lant
from .serializers import ReportsSerializer,UserLoginSerializer, UserSerializer ,I3lantHomeSerializer  , CatSerializer,StoresSerializer ,ItemsSerializer ,categoriesSerializer ,FavoriteListSerializer ,AddressSerializer ,OrderSerializer,ListOrderSerializer

from django.contrib.auth.hashers import check_password , make_password
from khafofi import sendnotification, get_token
from rest_framework.permissions import AllowAny
from django.db.models import Q

# Create your views here.







##========================auth================================================    
@api_view(["POST"])
@authentication_classes([])  # Empty list means no authentication classes
@permission_classes([AllowAny])
def check_account(request):
    try:
        user = User.objects.get(phone=request.data["phone"])
        if user.banned == True:
            return Response({"status": "banned"})
        else :
            return Response({"status": "exists"})
    except :
        return Response({"status": "not existing"})
    

@api_view(["POST"])
@authentication_classes([])  # Empty list means no authentication classes
@permission_classes([AllowAny])
def create_account(request):
    try:
        user_exists = User.objects.filter(phone=request.data["phone"]).exists()
        if user_exists:
            return Response({"status": "exists"})
        request.data["password"] = make_password(request.data["password"])
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( {"status": "success","user": serializer.data,"token" :  get_token.getToke()}) # 
        else :
            return Response({"status": "failure"})
    except :
        return Response({"status": "failure"})

@api_view(["POST"])
@authentication_classes([])  # Empty list means no authentication classes
@permission_classes([AllowAny])
def login(request):
    try:
        user = User.objects.get(phone=request.data["phone"])
        is_password_correct = check_password(request.data['password'], user.password) 
        if is_password_correct :
            if user.banned :
                return Response({"status": "banned"})
            else:
                serializer = UserLoginSerializer(user)
                return Response({"status": "success" , 'user' : serializer.data ,"token" :  get_token.getToke()}) 
        else :    
            return Response({"status": "wrong password"})
    except :
        return Response({"status": "not existing"})

@api_view(["POST"])
@authentication_classes([])  # Empty list means no authentication classes
@permission_classes([AllowAny])
def resetPassword(request):
    try:
        user = User.objects.get(phone=request.data["phone"])
        user.password = make_password(request.data['password']) 
        user.save()
        serializer = UserLoginSerializer(user)
        return Response({"status": "success" , 'user' : serializer.data , "token" :  get_token.getToke()})
    except :
        return Response({"status": "failure"})

##========================Home================================================ 
@api_view(["GET"])
def home(request , pk):
    try:    
        user = User.objects.get(id=pk)

        if user.banned == True :
            return Response({"status": "banned"})
        
        i3lana = I3lant.objects.all()
        serializerI3lana = I3lantHomeSerializer(i3lana , many = True)

        cat = Categories.objects.all()
        serializerCat = CatSerializer(cat , many = True)
        
        mostliked = Item.objects.order_by('-likes')[:5]
        serializermostliked = ItemsSerializer(mostliked, many=True , context={'user_id': pk}) 

        mostselling = Item.objects.order_by('-selling')[:5]
        serializermostselling = ItemsSerializer(mostselling, many=True , context={'user_id': pk}) 

       
        return Response({"status": "success","i3lanat": serializerI3lana.data ,"categories": serializerCat.data,"mostliked" : serializermostliked.data,"mostselling" : serializermostselling.data,})
    except :  
        return Response({"status": "failure"})
    
#========================stores================================================ 
@api_view(["GET"])
def stores(request , pk  ):
    try:      
        stores = Store.objects.filter(stores_cat=pk,).order_by('id')
        serializer = StoresSerializer(stores , many = True)
        return Response({"status": "success","stores": serializer.data,})
    except:
        return Response({"status": "failure"})    


#========================items================================================ 
@api_view(["POST"])
def items(request, pk):
    try:
        user_id = request.data["user_id"]
        items = Item.objects.filter(store=pk)
        categories = Category.objects.filter(~Q(count=0) ,store=pk , )

        serialized_categories = []
        for category in categories:
            category_data = categoriesSerializer(category).data
            category_items = items.filter(cat=category.id)
            category_data["items"] = ItemsSerializer(category_items, many=True, context={'user_id': user_id}).data
            serialized_categories.append(category_data)
        
        return Response({"status": "success","category": serialized_categories})
    except :  
        return Response({"status": "failure"})  
    
#========================favorite================================================     
@api_view(["POST" , 'DELETE'])
def fav_add_remove(request):
    try:
        user = User.objects.get(id=request.data["user_id"])
        item = Item.objects.get(id=request.data["item_id"])
        if request.method == "POST":
            Favorite.objects.create(user=user, item=item)
            item.add_like()
            return Response({"status": "success",})
        if request.method == 'DELETE':
            fav = Favorite.objects.get(user=user,item=item)
            fav.delete()
            item.remove_like()
        return Response( {"status": "success",})
    except :  
        return Response({"status": "failure"})   

@api_view(["GET"])
def listfav(request , pk ):
    try:
        user = User.objects.get(id=pk)
        favorite = Favorite.objects.filter(user=user)
        serializerfavorite = FavoriteListSerializer(favorite , many = True , context={'user_id': pk} )
        return Response({"status": "success","items": serializerfavorite.data})
    except :  
        return Response({"status": "failure"})       
    
   
#=================================address_User===================================

@api_view(["GET"])
def listAddress(request , pk ):
    try:
        user = User.objects.get(id=pk)
        address= Address.objects.filter(user_id=user)
        serializeraddress = AddressSerializer(address , many = True )
        return Response({"status": "success","addresses": serializeraddress.data})
    except :  
        return Response({"status": "failure"})      

@api_view(["POST" , "DELETE"])
def address_add_remove(request) :
    try:
        if request.method == "POST":    
            user_id = request.data['user_id']
            address_name = request.data['name']
            latitude = request.data['latitude']
            longitude = request.data['longitude']
            user = User.objects.get(id=user_id)
            existing_address = Address.objects.filter(user=user, name=address_name).exists()
            if existing_address:
                return Response({"status": "exists"})
            limited_address = Address.objects.filter(user=user).count()
            if limited_address >= 5:
                return Response({"status": "limited"})
            Address.objects.create(user=user, name=address_name, latitude=latitude, longitude=longitude)
            return Response({"status": "success"})
        if request.method == "DELETE":
            address_id = request.data['address_id']
            address = Address.objects.get(id=address_id)
            address.delete()
            return Response({"status": "success"})     
    except :
        return Response({"status": "failure"})





#=================================Order_User===================================
@api_view(['POST'])
def make_order(request):
    try :
        if not Delivery.objects.filter(open=True).exists():
            return Response({"status": "delivery_closed"})
        store = Store.objects.get(id=request.data["store"])
        if store.open == False :
            return Response({"status": "store_closed"}) 
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            sendnotification.send_notification(" ♠ توجد طلبية" ,f"يمكنك مراجعة الطلبية والبدأ في الإعداد" ,f"store{store.id}" , "/orderlist" , "refreshome")
            return Response({"status": "success"})
        else:
            return Response({"status": "failure"}) 
    except :
        return Response({"status": "failure"}) 



@api_view(['GET'])
def list_order_user(request , pk):
    try :   
        user = User.objects.get(id=pk)
        order= Order.objects.filter(user=user)
        serializerOrders = ListOrderSerializer(order , many = True)
        orders = serializerOrders.data
        return Response({"status": "success","orders": orders})        
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
            sendnotification.send_notification("يوجد إبلاغ" ,f"من قبل المستخدم" ,f"admin" , "" , "")
            return Response({"status": "success"})
        else :
            return Response({"status": "failure"}) 
    except :
        return Response({"status": "failure"})    
    

@api_view(['DELETE'])
def Cancel_Order(request ,pk):
    try:
        order = Order.objects.get(id=pk)
        if order.status == 0 :
            order.delete() 
            sendnotification.send_notification("تم إلغاء الطلبية" ,f"☻☺♦♣♠•◘○" ,f"store{order.store.id}" , "/orderlist" , "refreshome")
            return Response({"status": "success"})
        else :
             return Response({"status": "cannot"})
    except:
        return Response({"status": "failure" })        
    
#=================================settings===================================    

@api_view(["POST"])
def change_pass(request,pk):
    try:
        user = User.objects.get(id=pk)
        is_oldpassword_correct = check_password(request.data['oldpass'], user.password) 
        if is_oldpassword_correct:
            user.password = make_password(request.data['newpass'])
            user.save()
            return Response({"status": "success"})
        else :
            return Response({"status": "wrong password"})
    except :
        return Response({"status": "failure"})





#-----------test------------
    
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import messaging
# @api_view(['POST'])       
# def testmsg (request,pk) :
#     cred = credentials.Certificate("keys/firebasemessaging.json")
#     firebase_admin.initialize_app(cred)

# # Construct the message
#     message = messaging.Message(
#     notification=messaging.Notification(
#         title="New Delivery",
#         body="Your package has been dispatched.",
#     ),
#     topic="user",
#     )

# # Send the message
#     response = messaging.send(message)
#     print('Notification sent:', response)


