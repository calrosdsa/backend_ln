from django.db.models.expressions import F
from django.db.models.fields import CharField, FloatField, IntegerField
from django.shortcuts import get_object_or_404
from rest_framework import pagination

from novels.serializers import CategorySerializer, NovelChapterSerializer3, NovelSerializer4, TagSlugSerializer
from .models import Novel,Status
from categories.models import Category
from rest_framework.response import Response
from django.db.models import Max,Sum,Avg,Count
from tags.models import Tag
from django.db.models.functions import Coalesce,Cast,Concat,ExtractMonth

class LibraryPagination(pagination.PageNumberPagination):
    page_size=20
    def get_paginated_response(self, data):

        return Response({
            'results': data,
            'options': self.request.GET.get('options'),
            'ordering': self.request.GET.get('ordering'),

        })



class DefaultPagination(pagination.PageNumberPagination):
    page_size=20
    def get_paginated_response(self, data):
        next_page_query = (self.get_next_link().split('/')[-1]
                           if self.get_next_link() else None)

        previous_page_query = (self.get_previous_link().split('/')[-1]
                               if self.get_previous_link() else None)
        tag = Tag.objects.alias(popular_tags = Count('novels')).order_by('-popular_tags')
        tag = TagSlugSerializer(tag,many=True).data[:20]

        return Response({
            'pages_count': self.page.paginator.num_pages,
            'title': self.request.GET.get('title'),
            'current': self.page.number,
            'next': next_page_query,
            'previous': previous_page_query,
            'results': data
        })


class FilterAdvancedPagination(pagination.PageNumberPagination):
    page_size=30 
    def get_paginated_response(self, data):
        next_page_query = (self.get_next_link().split('/')[-1]
                           if self.get_next_link() else None)

        previous_page_query = (self.get_previous_link().split('/')[-1]
                               if self.get_previous_link() else None)
     
        category = Category.objects.all()
        category = CategorySerializer(category,many=True,read_only = True).data
        tags = Tag.objects.all()
        tags = TagSlugSerializer(tags,many=True,read_only=True).data
        


        return Response({
            'previous': previous_page_query,
            'next': next_page_query,
            'tags':tags,
            'category': category,
            'pages_count': self.page.paginator.num_pages,
            'products_count': self.page.paginator.count,
            'current': self.page.number,
            'novels': data
        })


class CustomPagination(pagination.PageNumberPagination):
    page_size=20
    def get_paginated_response(self, data):
        next_page_query = (self.get_next_link().split('/')[-1]
                           if self.get_next_link() else None)

        previous_page_query = (self.get_previous_link().split('/')[-1]
                               if self.get_previous_link() else None)
        novel = get_object_or_404(Novel.objects.annotate(statuss = Cast('status__status', output_field=CharField()),
            chapters = Count('novel_chapter__id'),updated=Max('novel_chapter__created_at')), id = data[0].get('novel'))
        novel = NovelSerializer4(novel)

        return Response({
            'novel': novel.data,
            'pages_count': self.page.paginator.num_pages,
            'products_count': self.page.paginator.count,
            'current': self.page.number,
            'next': next_page_query,
            'previous': previous_page_query,
            'chapters': data
        })


class TagPagination(pagination.PageNumberPagination):
    page_size=20
    def get_paginated_response(self, data):
        next_page_query = (self.get_next_link().split('/')[-1]
                           if self.get_next_link() else None)

        previous_page_query = (self.get_previous_link().split('/')[-1]
                               if self.get_previous_link() else None)
        tag = Tag.objects.alias(popular_tags = Count('novels')).order_by('-popular_tags')
        tag = TagSlugSerializer(tag,many=True).data[:20]

        return Response({
            'tag': tag,
            'pages_count': self.page.paginator.num_pages,
            'title': self.request.GET.get('title'),
           # 'current': self.page.number,
            #'next': next_page_query,
            #'previous': previous_page_query,
            'tags': data
        })

class NovelTagPagination(pagination.PageNumberPagination):
    page_size=10
    def get_paginated_response(self, data):
        next_page_query = (self.get_next_link().split('/')[-1]
                           if self.get_next_link() else None)

        previous_page_query = (self.get_previous_link().split('/')[-1]
                               if self.get_previous_link() else None)
        

        return Response({
            'pages_count': self.page.paginator.num_pages,
            'current': self.page.number,
            'next': next_page_query,
            'ordering': self.request.GET.get('ordering'),
            'previous': previous_page_query,
            'novels': data
        })

class FilterPagination(pagination.PageNumberPagination):
    page_size=30 
    def get_paginated_response(self, data):
        next_page_query = (self.get_next_link().split('/')[-1]
                           if self.get_next_link() else None)

        previous_page_query = (self.get_previous_link().split('/')[-1]
                               if self.get_previous_link() else None)
     
        category = Category.objects.values('title','id','slug')
        status =  Status.objects.values('status','id')


        return Response({
            'previous': previous_page_query,
            'next': next_page_query,
            'ordering': self.request.GET.get('ordering'),
            'status_': self.request.GET.get('status'),
            'category_': self.request.GET.get('category'),
            'status': status,
            'category': category,
            'pages_count': self.page.paginator.num_pages,
            'products_count': self.page.paginator.count,
            'current': self.page.number,
            'novels': data
        })
