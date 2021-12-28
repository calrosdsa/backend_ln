from .models import NovelNotifiactions
from rest_framework import serializers
from users.models import CustomUser
from novels.serializers import NovelSerializer2

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'last_login', 'date_joined', 'is_staff')

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model= NovelNotifiactions
        fields = ('novel','name','user','is_seen')