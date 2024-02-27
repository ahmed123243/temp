from django.db import models
from django.core.validators import  FileExtensionValidator 
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
def validate_image(image):
    file_size = image.size
    limit_mb = 5 * 1024 * 1024
    if file_size >= limit_mb :
       raise ValidationError("Max size of file is %s MB" % limit_mb)

# Create your models here.


class AdminManager(BaseUserManager):
    def create_user(self, fullname, phone, password=None, **extra_fields):
        if not fullname:
            raise ValueError('The Full Name must be set')
        if not phone:
            raise ValueError('The Phone must be set')

        user = self.model(
            fullname=fullname,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fullname, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(fullname, phone, password, **extra_fields)

class Admin(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=20)
    phone = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_updated = models.DateTimeField(auto_now=True)
    objects = AdminManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['fullname']

    def __str__(self):
        return self.fullname

    def get_full_name(self):
        return self.fullname

    def get_short_name(self):
        return self.fullname
    
@receiver(post_save, sender=Admin)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)   

class Categories(models.Model) :
   category_name_ar = models.CharField(max_length=20 , unique=True)
   category_name_en = models.CharField(max_length=20 , unique=True)
   image = models.FileField(blank=True,null=True,upload_to="categories/", validators=[FileExtensionValidator(['svg']) ,validate_image ])
   def __str__(self):
       return self.category_name_en
   

class I3lant(models.Model) :
    image =  models.ImageField(upload_to="I3lant/" , validators=[validate_image]) 

class OrderOut(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    delivery = models.ForeignKey("delivery.delivery", on_delete=models.CASCADE , blank=True,null=True )
    total = models.PositiveIntegerField()
    user_phone = models.CharField(max_length=10)
    user_name = models.CharField(max_length=20 ,blank=True,null=True)
    status = models.SmallIntegerField(default=2)
    created_at = models.DateTimeField(auto_now_add=True,)
    def __str__(self):
        return f"Order {self.admin.fullname}" 
    class Meta:
        ordering=["-created_at"]


class Historyadmin(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return  self.reason
    class Meta:
        ordering=["-date_created"]
