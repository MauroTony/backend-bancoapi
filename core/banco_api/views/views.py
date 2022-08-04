from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView, status

class HelloWorld(APIView):
    
    def get(self, request):
        return Response({"message": "Hello World!"})