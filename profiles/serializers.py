from rest_framework import serializers
from rest_framework.fields import ImageField
from .models import Profile,History
from novels.models import Comment,Review    

class CommentSerializerUser(serializers.ModelSerializer):
    added_b = serializers.CharField()
    count_likes = serializers.IntegerField()
    image = serializers.CharField()
    count_reply = serializers.IntegerField()
    novel_title=serializers.CharField()
    novel_cover = serializers.CharField()
    novel_slug = serializers.SlugField()
   # reply_comments = Comment_ReplySerializer(read_only = True, many=True)
    class Meta:
        model=Comment
        fields = ['id','count_reply', 'image','count_likes','added_b' ,'body', 'date_added','novel_title','novel_cover','novel_slug']
        read_only_fields = fields
        


class ReviewSerialiezerUser(serializers.ModelSerializer):
    avatar= serializers.CharField()
    user = serializers.CharField()
    like = serializers.IntegerField()
    novel_title=serializers.CharField()
    novel_cover = serializers.CharField()
    novel_slug = serializers.SlugField()
    class Meta:
        model=Review
        fields = ['id', 'avatar','novel','user','like', 'rating','review', 'date_added','novel_title','novel_cover','novel_slug']
        read_only_fields = fields
        

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'name', 'avatar', 'bio']


class HistorySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    cover = serializers.ImageField()
    user = serializers.CharField( source='user.username')       

    class Meta:
        model = History
        fields = ('id','content_type','object_id','cover','user','title')
        
    def get_title(self,obj):
        return obj.title
    def get_cover(self,obj):
        return obj.cover