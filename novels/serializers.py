from django.db.models import fields
from django.db.models.fields.files import ImageField
from rest_framework import serializers
from rest_framework.fields import CharField, FloatField, IntegerField
from rest_framework.response import Response
from .models import  Library, LibraryModel, Novel,NovelChapter,Reply_Comment,Reply_Review,Comment,Review
from tags.models import Tag
from categories.models import Category
from django.contrib.auth import get_user_model

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'title',
            'id',
        )
        

class TagSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'title',
            'slug',
            'id',
        )



class Comment_ReplySerializer(serializers.ModelSerializer):
    image= serializers.CharField(read_only=True)
    added_b = serializers.CharField(read_only=True)
    like = serializers.IntegerField()
    
    class Meta:
        model=Reply_Comment
        fields=[ 'id', 'image', 'added_b','like', 'reply', 'date_added']



class Review_ReplySerializer(serializers.ModelSerializer):
    avatar= serializers.ImageField(read_only=True, source="profile.avatar")
    
    class Meta:
        model=Reply_Review
        fields=[ 'id', 'avatar', 'added_by','likes', 'reply', 'date_added']



class CommentSerializer(serializers.ModelSerializer):
    added_b = CharField()
    count_likes = serializers.IntegerField()
    image = serializers.CharField()
    count_reply = serializers.IntegerField()
   # reply_comments = Comment_ReplySerializer(read_only = True, many=True)
    class Meta:
        model=Comment
        fields = ['id','count_reply','added_by', 'image','count_likes','added_b' ,'body', 'date_added']
        read_only_fields = fields
        


class ReviewSerialiezer(serializers.ModelSerializer):
    avatar= serializers.CharField()
    user = serializers.CharField()
    like = serializers.IntegerField()
    class Meta:
        model=Review
        fields = ['id', 'avatar','novel','user','like', 'rating','review', 'date_added']
        read_only_fields = fields
        

class NovelChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model=NovelChapter
        fields= ['created_at','novel', 'id','title','slug','number']
        read_only_fields = fields


class NovelChapterSerializer2(serializers.ModelSerializer):
    novel_title = serializers.CharField()
    novel_cover = serializers.CharField()
    novel_slug = serializers.SlugField()
    class Meta:
        model=NovelChapter
        fields= ('id','novel_title','slug','novel_cover','novel','created_at','title','novel_slug')
        read_only_fields = fields


class NovelChapterSerializer3(serializers.ModelSerializer):
    novel_title = serializers.CharField()
    novel_cover = serializers.CharField()
    novel_slug = serializers.CharField()
    class Meta:
        model=NovelChapter
        fields= ('id','novel_title','chapter','novel_cover','novel','created_at','title','novel_slug')
        read_only_fields = fields
          
    
class RatingSerializer(serializers.ModelSerializer):
    reviews = serializers.IntegerField()
    average = serializers.FloatField()
    class Meta:
        model=Novel
        fields= ['cover','id', 'title','reviews','average','slug']    
        read_only_fields = fields
        
    
class TrendsSerializer(serializers.ModelSerializer):
    reviews = serializers.IntegerField()
    commentss = serializers.IntegerField()
    class Meta:
        model=Novel
        fields= ['cover','slug', 'title','reviews','commentss']    
        read_only_fields = fields
        
class WeeklySerializer(serializers.ModelSerializer):
    chapters = serializers.IntegerField()
    average = serializers.FloatField()
    class Meta:
        model=Novel
        fields= ['cover','slug','id' ,'title','chapters','average','rank']    
        read_only_fields = fields
        
class NovelFilterSerializer(serializers.ModelSerializer):
    chapters = serializers.IntegerField()
    reviews = serializers.IntegerField()
    commentss= serializers.IntegerField()
    average = serializers.FloatField()
    class Meta:
        model=Novel
        fields= ['cover','slug','id' ,'title','chapters','average','rank','update_at',' ','commentss','reviews']    
        read_only_fields = fields
        

class NovelSerializer3(serializers.ModelSerializer):
    avg = serializers.DecimalField(decimal_places=1,max_digits=2)
    class Meta:
        model=Novel
        fields= ['cover','id','avg','rank','slug' ,'title','update_at']
        read_only_fields = fields 

class NovelSerializer4(serializers.ModelSerializer):
    statuss = serializers.CharField()
    chapters = serializers.IntegerField()
    updated = serializers.DateTimeField()
    class Meta:
        model=Novel
        fields= ['cover','statuss','id','rank','slug' ,'title','updated','chapters']
        read_only_fields = fields
        
        

class NovelSerializer0(serializers.ModelSerializer):
    comentarios = serializers.IntegerField()
    reviews = serializers.IntegerField()
    chapters = serializers.IntegerField()
    status_name = serializers.CharField()
    updated = serializers.DateTimeField()
    class Meta:
        model=Novel
        fields= ['cover','slug','id', 'title','created','updated','comentarios','reviews','chapters',
                'status_name','average','rank']
        read_only_fields = fields
        
class NovelSerializer2(serializers.ModelSerializer):
    chapter_count = serializers.IntegerField()
    markeds = serializers.IntegerField()
    class Meta:
        model=Novel
        fields= ['cover','id','slug', 'title','novel_views','chapter_count','markeds']
        
class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Novel
        fields= ['cover','id', 'title','novel_views']

class NovelSerializer(serializers.ModelSerializer):
    tags = TagSlugSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True, many=True)
    average = serializers.FloatField()
    reviews = serializers.IntegerField()
    chapters = serializers.IntegerField()
    authors = serializers.CharField()
    statuss = serializers.CharField()
    updated = serializers.DateTimeField()
    

    class Meta:
        model=Novel
        fields= ['cover','slug','novel_views','tags','created','updated','category','authors','statuss','sub','description',
         'id','sumary','rank', 'title','average','average','book_marked','reviews','chapters' ]

        read_only_fields = fields
    def get_is_favorite_product(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Library.objects.check_product(user, obj.id)
        return False
class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=LibraryModel
        fields=['option']

class NovelSerializerFav(serializers.ModelSerializer):
    progress = serializers.IntegerField()
    chapters = serializers.IntegerField()
    added = serializers.CharField()
    options = serializers.ListField(
        child=serializers.IntegerField()
        )
    updated = serializers.DateTimeField()
    class Meta:
        model=Novel
        fields= ['cover','id','progress','slug','options' ,'title','chapters','added','updated']
        
        read_only_fields = fields 

class LibrarySerializer(serializers.ModelSerializer):
    novel= NovelSerializerFav(many=True, required=False)
    class Meta:
        model=Library   
        fields= ['novel']
class NovelChapterUser(serializers.ModelSerializer):
    
    class Meta:
        model = NovelChapter
        fields = ['slug','title']
