from rest_framework import serializers
from rest_framework.fields import ImageField
from .models import HistoryNovel, Profile,History
from novels.models import Comment,Review    

class CommentSerializerUser(serializers.ModelSerializer):
    added_b = serializers.CharField()
    count_likes = serializers.IntegerField()
    count_reply = serializers.IntegerField()
    novel_title=serializers.CharField()
    novel_slug = serializers.SlugField()
   # reply_comments = Comment_ReplySerializer(read_only = True, many=True)
    class Meta:
        model=Comment
        fields = ['id','count_reply','count_likes','added_b' ,'body', 'date_added','novel_title','novel_slug']
        read_only_fields = fields
        


class ReviewSerialiezerUser(serializers.ModelSerializer):
    user = serializers.CharField()
    like = serializers.IntegerField()
    novel_title=serializers.CharField()
    novel_slug = serializers.SlugField()
    class Meta:
        model=Review
        fields = ['id','novel','user','like', 'rating','review', 'date_added','novel_title','novel_slug']
        read_only_fields = fields
        

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'name', 'avatar', 'bio']


class HistorySerializer(serializers.ModelSerializer):
    novel_title = serializers.CharField()
    rank = serializers.IntegerField()
    novel_slug = serializers.CharField()
    novel_cover = serializers.CharField()
    chapters = serializers.IntegerField()
    progress = serializers.IntegerField()
    last_chapter = serializers.CharField()
    last_chapter_slug = serializers.CharField()

    class Meta:
        model = HistoryNovel
        fields = ['last_chapter','novel_cover','rank','last_chapter_slug','viewed_on','novel_title','novel_slug','chapters','progress','novel']
        