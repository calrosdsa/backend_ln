from django.db.models.deletion import DO_NOTHING
import time
from .filter import AdvaceFilter, NovelFilter
import math
from django.db.models.expressions import OuterRef, Subquery, Value
from django.utils import timezone
from datetime import timedelta
from django.db.models.fields import CharField, SlugField, TextField
from django.db.models.fields.files import ImageField
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, request
from django_filters.rest_framework.backends import DjangoFilterBackend,filters
from rest_framework.compat import distinct
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from novels.paginations import CustomPagination, FilterAdvancedPagination, FilterPagination, NovelTagPagination
from .models import  Authors, Library, Novel, NovelChapter, Reply_Comment, Reply_Review,Review,Comment, Status
from .serializers import Comment_ReplySerializer, NovelChapterSerializer, NovelChapterSerializer2,NovelChapterSerializer3, NovelFilterSerializer, NovelSerializer,CommentSerializer, NovelSerializer0, NovelSerializer2, NovelSerializer3, NovelSerializerFav, RatingSerializer, ReviewSerialiezer, TrendsSerializer, WeeklySerializer
from tags.models import Tag
from categories.models import Category
from rest_framework import  pagination, serializers, status
from rest_framework.views import APIView
import json #Useful for POST and PUT requests
from rest_framework.generics import ListAPIView,RetrieveAPIView
from django.apps import apps 
from django.db.models.functions.window import RowNumber
from django.db.models.functions import Coalesce,Cast,Concat,ExtractMonth
from django.db.models import Avg, Count,Sum,F,Window,Q
from rest_framework import mixins, generics
from profiles.signals import object_viewed_signal
Users = apps.get_model('users', 'CustomUser')
Profile = apps.get_model('profiles', 'Profile')
# Create your views here.


class DetailNovels(APIView):
  #  def dispatch(self, request, *args, **kwargs):
   #         instance = Novel.objects.get(slug=kwargs['slug'])
    #        if request.user.is_authenticated and instance is not None:
     #          object_viewed_signal.send(instance.__class__, instance=instance, request=request)
      #      return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,*args, **kwargs):
            novel = get_object_or_404(Novel.objects.annotate(statuss = Cast('status__status',output_field=CharField())
            ,authors = Cast('author__author',output_field=CharField())
            ,avg = Avg('review__rating'),reviews = Count('review',distinct=True),
            chapters = Count('novel_chapter',distinct=True)
            ),slug = kwargs['slug'])
            Novel.update_avg(novel.id,novel.avg,novel.novel_views)
            serializer = NovelSerializer(novel)
            comment= Comment.objects.filter(novel = novel.id).annotate(added_b = Cast('added_by__username',output_field=CharField()),
            count_likes = Count('likes',distinct=True),image = Concat(Value('/media/'),'profile__avatar', output_field=CharField()),
            count_reply = Count('reply_comments__id',distinct=True)).order_by('-date_added')
            novel = CommentSerializer(comment, many=True,read_only=True).data
            #comment_reply = Reply_Comment.objects.filter(comment = comment).annotate(like = Count('likes'),added_b=Cast('added_by__username',output_field=CharField()),
             #   avatar = Concat(Value('/media/'),'profile__avatar',output_field=CharField())).values()
           # reply_serialier = Comment_ReplySerializer(comment_reply,many=True)
            #print(comment_reply)
            data =serializer.data
            #data['reply'] = reply_serialier.data
            data['comments'] =novel
            return Response(data)


class Ranking(APIView):
        #qs = novel.filter(rank = 1)
       # print(qs.rank)
        #novel.update(rank = novel.ranking)
    def get(self,request):
        lasts = timezone.now() - timedelta(days=10)
        last_month = timezone.now() - timedelta(days=30)
        
        novels = Novel.objects.annotate(chapters =
        Count('novel_chapter',distinct=True)).order_by('-created')
        serializer = WeeklySerializer(novels,many=True, read_only = True).data[:12]
        #,mothly = ExtractMonth('update_at',distinct=True)).filter(created__gt = last_month)
        q = Novel.objects.filter(created__gt = last_month ).alias(ordering = Count('comments')+Count('review')).annotate(commentss = Count('comments',distinct=True), reviews=Count('review',distinct=True)
        ).filter(Q(review__date_added__gt = lasts) | Q(comments__date_added__gt= lasts )).order_by('-ordering')
        serializer1 = TrendsSerializer( q,many=True, read_only=True).data[:10]
        novels = Novel.objects.alias(most_rated = Count('review') + F('average') * 15).filter(Q(average__range = (4.5,5.0))).annotate(reviews = Count('review__id')
            ).order_by('-most_rated')
        serializer2 = RatingSerializer(novels,many=True, read_only=True).data[:10]
        novel = Novel.objects.annotate(chapter_count = Count('book_marked',distinct=True),markeds = Count('book_marked',distinct=True)).order_by('-novel_views')
        serializer3 = NovelSerializer2(novel,many=True).data[:10]
        weekly = Novel.objects.annotate(chapters = Count('novel_chapter__id',distinct=True)
        ).filter(Q(review__date_added__gt = lasts) | Q(novel_chapter__created_at__gt= lasts )| Q(comments__date_added__gt= lasts ))
        serializer4 = WeeklySerializer( weekly,many=True).data[:12]
        completed = Novel.objects.annotate(chapters = Count('novel_chapter__id',distinct=True)
        ).filter(status__status = 'Completed')
        serializer5 = WeeklySerializer(completed,many=True).data[:12]
        chapters = NovelChapter.objects.annotate(novel_title=Cast('novel__title',output_field=CharField()),
            novel_cover = Concat(Value('/media/'),'novel__cover',output_field=CharField()),novel_slug=Cast('novel__slug',output_field=SlugField())).order_by('-created_at')
        serializer6 = NovelChapterSerializer2(chapters,many=True).data  
        return Response({'posts':serializer,
                         'trends':serializer1,
                         'rated':serializer2,
                         'popular':serializer3,
                         'weekly':serializer4,
                         'completed':serializer5,
                         'chapters':serializer6,
                         })




class NovelView(ListAPIView):
    queryset = NovelChapter.objects.all()
    serializer_class = NovelChapterSerializer
    pagination_class=CustomPagination
    def get_queryset(self):
        qs = super(NovelView, self).get_queryset()
        slug=self.kwargs.get('slug')
        novel = Novel.objects.get(slug=slug) 
        return qs.filter(novel=novel)
        

class Filter(ListAPIView):
    last_month = timezone.now() - timedelta(days=30)
    queryset = Novel.objects.annotate(popular = Count('review')*2+  Count('comments'),reviews = Count('review',distinct=True),chapters = Count('novel_chapter__id',distinct=True),
    comentarios = Count('comments__id',distinct=True),status_name = Cast('status__status',output_field=CharField())).order_by('-created')
    serializer_class = NovelSerializer0
    pagination_class = FilterPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = NovelFilter
    
class AdvancedFilter(ListAPIView):
    last_month = timezone.now() - timedelta(days=30)
    queryset = Novel.objects.annotate(popular = Count('review')*2+  Count('comments'),reviews = Count('review',distinct=True),chapters = Count('novel_chapter__id',distinct=True),
    comentarios = Count('comments__id',distinct=True),status_name = Cast('status__status',output_field=CharField())).order_by('-created')
    serializer_class = NovelSerializer0
    pagination_class = FilterAdvancedPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvaceFilter
          
class ChapterView(RetrieveAPIView):
    queryset = NovelChapter.objects.annotate(novel_title = Cast('novel__title',output_field=CharField()),
            novel_cover = Concat(Value('/media/'),"novel__cover", output_field=CharField()))
    serializer_class = NovelChapterSerializer3
    lookup_field = ('slug')




class PostList(ListAPIView):
    pagination_class = NovelTagPagination
    serializer_class = NovelSerializer0
    filter_backends = [DjangoFilterBackend]
    filterset_class = NovelFilter
    
    def get_queryset(self):
        qs = Novel.objects.annotate(popular = Count('review')*2+  Count('comments'),reviews = Count('review__id',distinct=True),chapters = Count('novel_chapter__id',distinct=True),
    comentarios = Count('comments__id',distinct=True),status_name = Cast('status__status',output_field=CharField())).order_by('-popular')
        # Filter by tag
        tag = self.kwargs.get('tag')
        if tag:
            tag = Tag.objects.get(slug=tag)
            return qs.filter(tags=tag)
        
        author = self.kwargs.get('author')
        if author:
            author = Authors.objects.get(slug=author)
            return qs.filter(authors=author)
        return qs[:12]


class FavoritesProductsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        qs = get_object_or_404(Library, user=user).products.all()
        products = NovelSerializerFav(
            qs, context={'request': request}, many=True).data
        return JsonResponse({'profile': products}, safe=False,status=status.HTTP_200_OK)


class UpdateFavoritesProductsView(APIView):
    """Get product then if product in favorites novels exists remove from that, 
    else add it to favorites novels"""

    permission_classes = (IsAuthenticated,)
    def post(self, request, id):
        user = request.user
        product = get_object_or_404(Novel, id=id)
        obj, _ = Library.objects.get_or_create(user=user)
        if obj.products.filter(id=id).exists() or product.book_marked.filter(id=request.user.id).exists():
            product.book_marked.remove(user)
            obj.products.remove(product)
        else:
            obj.products.add(product)
            product.book_marked.add(user)
        product = NovelSerializerFav(
            product, context={'request': request})
        return Response(product.data)
        
class CreateComment(APIView):
    def post(self,request,*args, **kwargs):
        payload = json.loads(request.body)
        user = Users.objects.get(id = request.user.id)
        novel = Novel.objects.get(id = kwargs['id'])
        profile = Profile.objects.get(user = user.id)
        Comment.objects.create(novel = novel, added_by =user, body = payload['body'], profile = profile)
        return Response('comment created')
    def put(self,request,*args, **kwargs):
        comment = get_object_or_404(Comment,id = kwargs["id"])
        user = request.user
        if comment.likes.filter(id=request.user.id).exists(): # user already exists in the like list
           comment.likes.remove(user)
        else:
           comment.likes.add(user) # add the like to the like array in the review object
        return Response('added' )
    
class CommentView(APIView):
    def get(self , request,*args, **kwargs):
        comment = get_object_or_404(Comment.objects.annotate(count_likes = Count('likes',distinct=True),added_b = Cast('added_by__username',output_field=CharField()),
            image = Concat(Value('/media/'),'profile__avatar',output_field=CharField()), count_reply = Count('reply_comments__id',distinct=True)),id=kwargs['id'])
        serializer = CommentSerializer(comment).data
        comment_reply = Reply_Comment.objects.filter(comment = comment).annotate(like = Count('likes'),added_b=Cast('added_by__username',output_field=CharField()),
               avatar = Concat(Value('/media/'),'profile__avatar',output_field=CharField()))
        reply_serialier = Comment_ReplySerializer(comment_reply,many=True)
        serializer['reply_comments'] = reply_serialier.data
        return Response(serializer)
    def post(self,request,*args, **kwargs):
        payload = json.loads(request.body)
        user = Users.objects.get(id = request.user.id)
        profile = Profile.objects.get(id = user.id)
        comment = Comment.objects.get(id=kwargs['id'])
        Reply_Comment.objects.create(comment = comment, added_by = user, profile = profile, reply=payload['reply'])
        return Response('reply created succesfully')
    
    def put(self,request,*args, **kwargs):
        reply = get_object_or_404(Reply_Comment, id=kwargs['id'])
        user = request.user
        if reply.likes.filter(id=request.user.id).exists():
            reply.likes.remove(user)
        else: 
            reply.likes.add(user)
        return Response('like added')



   
class CreateReview(APIView):
    def post(self,request,*args, **kwargs):
        payload= json.loads(request.body)
        user =Users.objects.get(id=request.user.id)
        data= request.data
        novel = Novel.objects.get(slug=kwargs['slug'])

        alreadyExists = novel.review.filter(added_by=user).exists()
        if alreadyExists:
            content = {'detail': 'Product already reviewed'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        elif data['rating'] == 0:
            content = {'detail': 'Please select a rating'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        else:
        # In the Comment object, for some weird effin reason Django needs to get the specific INSTANCE of the object NOT the Key like the update object. WEIRDO DJANGO UGH
            profile = Profile.objects.get(user=user.id)
            Review.objects.create(novel=novel, added_by=user, review=payload['review'], profile=profile,
            rating=payload['rating'])
            serializer = NovelSerializer(novel)
            data = serializer.data
        return JsonResponse({'post': data}, safe=False, status=status.HTTP_201_CREATED)
        

    def get(self,request,*args, **kwargs):
        novel = get_object_or_404(Novel.objects.annotate(avg = Avg('review__rating')) , slug =kwargs['slug'])
        serializer1 = NovelSerializer3(novel).data
        reviews = Review.objects.annotate(user = Cast('profile__name',output_field=CharField()),
        avatar = Concat(Value('/media/'),'profile__avatar',output_field=CharField()),
        like=Count('likes',distinct=True)).filter(novel = novel).order_by('-date_added')
        serializer = ReviewSerialiezer(reviews, many =True).data
        serializer1['reviews']= serializer
        return Response(serializer1)
    
    def put(self,request,review_id):
        user = request.user
        review = get_object_or_404(Review, id = review_id)
        if review.likes.filter(id=request.user.id).exists(): # user already exists in the like list
           review.likes.remove(user)
        else:
           review.likes.add(user) # add the like to the like array in the review object
        return Response('added' )



class UpdateRank(APIView):  
        #qs = novel.filter(rank = 1)
       # print(qs.rank)
        #novel.update(rank = novel.ranking)
    def get(self,request):
  #      row =  Window(
   #         expression=RowNumber(),
    #        order_by=F('novel_views').desc()
     #   )
      #  query = Novel.objects.filter(id = OuterRef('pk')).order_by().annotate(ranking = row).values('ranking')
       # print(Subquery(query))
        #Novel.objects.update(rank = Subquery(query))
        novel = Novel.objects.annotate(ranking = Window(
            expression=RowNumber(),
            order_by=F('novel_views').desc()
        )).order_by('ranking')
        for result in novel.iterator():
            novel = Novel.objects.get(id = result.id)
            novel.rank =  result.ranking
            Novel.objects.filter(id = novel.id).update(rank = result.ranking)
        return Response('hello')
        #return Response(q)

class SearchNovel(APIView):
    def get(self,request):
       novel = Novel.objects.annotate(chapters = Count('novel_chapter')).order_by('rank')
       serializer = WeeklySerializer(novel,many=True).data
       serializer2 = WeeklySerializer(novel,many=True,read_only=True).data[:10]
       return Response({'popular':serializer2,'allnovels':serializer})







