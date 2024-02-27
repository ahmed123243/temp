from django.db import models
from store.models import Item, Store
from delivery.models import Delivery

class User(models.Model):
    fullname = models.CharField(max_length=20)  
    phone = models.CharField(max_length=10,unique=True)  
    password = models.CharField(max_length=255,) 
    banned  = models.BooleanField(default=False)
    date_updated = models.DateTimeField(blank=True,null=True,auto_now=True)

    def __str__(self) -> str:
        return self.fullname
    class Meta:
        ordering=["-date_updated"]



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    def __str__(self):
       return self.user.fullname +" "+ self.item.name
    class Meta:
        # Define unique together constraint
        unique_together = ('user', 'item')

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    def __str__(self) -> str:
        return self.user.fullname +" "+ self.name
    class Meta:
        ordering=["id"]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE , blank=True,null=True )
    items = models.JSONField()
    total = models.PositiveIntegerField()
    userlat = models.DecimalField(max_digits=9, decimal_places=7 )
    userlong = models.DecimalField(max_digits=10, decimal_places=7)
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True,)
    def __str__(self):
        return f"Order {self.user.fullname}" 
    class Meta:
        ordering=["-created_at"]

        
class Reports(models.Model) :
   order = models.ForeignKey(Order, on_delete=models.CASCADE)
   report_from = models.CharField(max_length=20)
   report_to = models.CharField(max_length=20)
   reason = models.CharField(max_length=30)
   created_at = models.DateTimeField(auto_now_add=True,)
   class Meta:
        ordering=["-created_at"]
        unique_together = ('order', 'report_from' , 'report_to')
   
   
