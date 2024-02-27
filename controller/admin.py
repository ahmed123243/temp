from django.contrib import admin

from .models import Admin ,Historyadmin , Categories,I3lant , OrderOut

class AdminAdmin(admin.ModelAdmin):
    model = Admin
    list_display = ['fullname', 'date_updated']


admin.site.register(Admin,AdminAdmin )
admin.site.register(Categories)
admin.site.register(I3lant)
admin.site.register(Historyadmin)
admin.site.register(OrderOut)

# Register your models here.
