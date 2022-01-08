from django.db.models.expressions import Value
from django.db.models.fields import CharField, SlugField
from django.db.models.functions.comparison import Cast
from django.db.models.functions.text import Concat
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from novels.filter import TagFilter
from novels.paginations import DefaultPagination, TagPagination
from novels.serializers import NovelChapterSerializer2
from tags.models import Tag
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .serializers import CategorySerializer,TagSerializer,StatusSerializer
from novels.models import NovelChapter
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from novels.models import Novel
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class TagView(ListAPIView):
    queryset = Tag.objects.alias(popular_tags = Count('novels')).order_by('-popular_tags')
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TagFilter
    pagination_class =TagPagination
 #   def get(self,request,*args, **kwargs):
  #      tag = Tag.objects.annotate(popular_tags = Count('novels')).order_by('-popular_tags')
   ##    return Response(serializer.data)

class NovelChapterUpdate(ListAPIView):
    queryset =  NovelChapter.objects.annotate(novel_title = Cast('novel__title',output_field=CharField())
            ,novel_cover = Concat(Value('/media/'),'novel__cover',output_field=CharField()),
            novel_slug = Cast('novel__slug',output_field=SlugField())).reverse()
    serializer_class =NovelChapterSerializer2
    pagination_class = DefaultPagination

    
    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



