from rest_framework import serializers
from tags.models import Tag
from .models import Category
from novels.models import Status

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'title',
            'slug',
        )
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = (
            'status',
            'slug',
        )

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields = (
            'title',
            'slug'
        )

        
        

