from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from notifications.serializers import NotificationsSerializer
from .models import NovelNotifiactions
from rest_framework.permissions import IsAuthenticated

class NotificationNovel(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        user = request.user
        notification = NovelNotifiactions.objects.filter(user = user)
        for result in notification:
            notify =NovelNotifiactions.objects.get(id=result.id)
            notify.is_seen = False
            notify.delete()
        serializer = NotificationsSerializer(notification,context={'request': request},many=True,)
        data = serializer.data
        return Response(data)
    