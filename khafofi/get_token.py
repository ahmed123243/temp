from rest_framework.authtoken.models import Token
from controller.models import Admin 
def getToke():
    return Token.objects.get(user=Admin.objects.get(pk=1)).key

   

