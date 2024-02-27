from django.contrib import admin
from user.models import *

class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['fullname', 'phone']


admin.site.register(User,UserAdmin )
admin.site.register(Reports)
admin.site.register(Favorite)
admin.site.register(Address)
admin.site.register(Order)


# Register your models here.
