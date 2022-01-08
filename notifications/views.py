from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from notifications.serializers import NotificationsSerializer
from .models import NovelNotifiactions
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)



class TestView(APIView):
    #@method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        # Locate name in redis database
        notifications = NovelNotifiactions.objects.all().values()
        return Response(notifications)

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, *args, **kwargs):
        return super(TestView, self).dispatch(*args, **kwargs)

        # If not found 
       
#class FurtherReadingViewSet(viewsets.ReadOnlyModelViewSet):
    
 #   serializer_class = FurtherReadingSerializer
  #  permission_classes = [IsAuthenticated]

   # def get_queryset(self):
    #    return FurtherReading.objects.all().filter(
     #       case__id=self.kwargs["case"],
      #      case__species__species__exact=self.kwargs["species"],
       # )

   # @method_decorator(cache_page(CACHE_TTL))
    #def dispatch(self, request, *args, **kwargs):
     #   return super().dispatch(request, *args, **kwargs)

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
    