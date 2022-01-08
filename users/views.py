from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from users.serializers import UserSerializer
User = get_user_model()
# Create your views here.

class UserView(APIView):
    def get(self , request):
        user = request.user.id
        user = User.objects.get(id=user)
        serializer = UserSerializer(user)
        return Response(serializer.data)