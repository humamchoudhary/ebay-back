from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework import status
from .serializers import UserSerializer,ItemSerializer

@api_view(["GET"])
def getData(request):
    return Response({"Name":"Humam"})



@api_view(["POST"])
def postUserLogin( request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Check credentials and return user object or error response
        user = authenticate(username=username, password=password)
        if user is not None:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def postUserSignup( request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() 
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
@api_view(["POST"])
def postItem( request):
        item = ItemSerializer(data=request.data)
        if item.is_valid():
            item.save()
            return Response(item.data, status=status.HTTP_201_CREATED)
        else:
            return Response(item.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth.models import User 
@api_view(["GET"])
def getUsers(request):
        users = User.objects.all()
        data = {
            "users": list(users.values("id", "username", "email"))  
        }
        return Response(data)