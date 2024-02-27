from django.db import models
from controller.models import Admin
# Create your models here.
class Delivery(models.Model):
  fullname = models.CharField(max_length=20)  
  phone = models.CharField(max_length=10,unique=True)  
  password = models.CharField(max_length=255) 
  points =  models.IntegerField(default=2)
  open = models.BooleanField(default=False)
  date_updated = models.DateTimeField(auto_now=True)
  banned  = models.BooleanField(default=False)
    
  def __str__(self) -> str:
    return self.fullname
  class Meta:
    ordering=["-date_updated"]

  def add_points(self, amount):
    self.points += amount
    self.save()

  def subtract_points(self, amount):
    if self.points > 0:
      self.points -= amount
      self.save()


          