from rest_framework.compat import distinct

from .models import Novel
import django_filters
from django.db.models import Avg, Count,Sum,F,Window,Q
from django.db.models.functions.window import RowNumber

from categories.models import Category
from .models import Status
from tags.models import Tag
from rest_framework.response import Response
STATUS_CHOICES = (
    (0, 'Regular'),
    (1, 'Manager'),
    (2, 'Admin'),
)


class LibraryFilter(django_filters.FilterSet):
    options = django_filters.NumberFilter(field_name='options',lookup_expr='icontains')
    ordering = django_filters.OrderingFilter(fields=(
            ('created'),
            ('updated'),
            ('added'),          
        ),

        # labels do not need to retain order
        field_labels={
            'ordering': 'Novels',
        }) 
    class Meta:
        model = Novel
        fields = ['ordering','options',]
        
        
class TagFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title',lookup_expr='startswith')
     
    class Meta:
        model = Tag
        fields = ['title']

class AdvaceFilter(django_filters.FilterSet):
    CHOICES = {
        ('exact', 'exact'), ('not_exact', 'not_exact')
    }
    category = django_filters.ModelMultipleChoiceFilter(queryset = Category.objects.all(), label="Filter by tag",
    method="filter_category")
    def filter_category(self, queryset, name, value):
        if not value:
           return queryset

        category_list = self.data.getlist('category')  # [v.pk for v in value]
        type_of_search = self.data.get('type_of_search')

        if type_of_search == 'exact':
           queryset = queryset.filter(category__in=category_list)

           for category in category_list:
               queryset = queryset.filter(category__id=category)
        else:
            queryset = queryset.filter(category__id__in=category_list).distinct()

        return queryset
   
    status = django_filters.ModelChoiceFilter(queryset = Status.objects.all())
    type_of_search = django_filters.ChoiceFilter(label="Exact match?", choices=CHOICES, method=lambda queryset, name, value: queryset)
    tags = django_filters.ModelMultipleChoiceFilter(queryset = Tag.objects.all(), label="Filter by tag",
    method="filter_tags")
   
    
    def filter_tags(self, queryset, name, value):
        if not value:
           return queryset

        tag_list = self.data.getlist('tags')  # [v.pk for v in value]
        type_of_search = self.data.get('type_of_search')

        if type_of_search == 'exact':
           queryset = queryset.filter(tags__in=tag_list)

           for tag in tag_list:
               queryset = queryset.filter(tags__id=tag)
        else:
            queryset = queryset.filter(tags__id__in=tag_list).distinct()

        return queryset
    
    ordering = django_filters.OrderingFilter(fields=(
            ('created'),
            ('updated'),
            ('popular'),
            ('rank'),
            ('book_marked'),
            ('reviews'),
            ('title'),
            ('average'),
        ),
        # labels do not need to retain order
        field_labels={
            'ordering': 'Novels',
        }) 
    average = django_filters.RangeFilter()
    class Meta:
        model = Novel
        fields = ['ordering','category','tags','status','average']          
    


class NovelFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset = Category.objects.all())

    status = django_filters.ModelChoiceFilter(queryset = Status.objects.all())
    ordering = django_filters.OrderingFilter(fields=(
            ('created'),
            ('updated'),
            ('popular'),
        ),

        # labels do not need to retain order
        field_labels={
            'ordering': 'Novels',
        }) 
    class Meta:
        model = Novel
        fields = ['ordering','category','status',]
            
        
class NovelFilter2(django_filters.FilterSet):

    ordering = django_filters.OrderingFilter(fields=(
            ('created'),
            ('update_at'),
            ('popular'),
        ),

        # labels do not need to retain order
        field_labels={
            'ordering': 'Novels',
        }) 
    class Meta:
        model = Novel
        fields = ['ordering']
            
        

    