from django.db.models.aggregates import Max, Min
#from asgiref.sync import async_to_sync
#from channels.layers import get_channel_layer
from django.contrib.postgres.aggregates import ArrayAgg
from profiles.models import History, HistoryNovel
from .filter import AdvaceFilter, LibraryFilter, NovelFilter
from django.db.models.expressions import CombinedExpression, Exists, OuterRef, Subquery, Value
from django.utils import timezone
from datetime import timedelta,datetime
from django.db.models.fields import CharField, DateTimeField, IntegerField, SlugField, TextField
from django.db.models.fields.files import ImageField
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, request
from django_filters.rest_framework.backends import DjangoFilterBackend,filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from novels.paginations import CustomPagination, FilterAdvancedPagination, FilterPagination, LibraryPagination, NovelTagPagination
from .models import  Authors, Library, LibraryModel, Novel, NovelChapter, Reply_Comment, Reply_Review,Review,Comment, Status
from .serializers import Comment_ReplySerializer, NovelChapterSerializer, NovelChapterSerializer2,NovelChapterSerializer3, NovelChapterUser, NovelFilterSerializer, NovelSerializer,CommentSerializer, NovelSerializer0, NovelSerializer2, NovelSerializer3, NovelSerializerFav, RatingSerializer, ReviewSerialiezer, TrendsSerializer, WeeklySerializer
from tags.models import Tag
from rest_framework import  pagination, serializers, status
from rest_framework.views import APIView
import json #Useful for POST and PUT requests
from rest_framework.generics import ListAPIView,RetrieveAPIView
from django.apps import apps 
from django.db.models.functions.window import RowNumber
from django.db.models.functions import Coalesce,Cast,Concat,ExtractMonth
from django.db.models import Avg, Count,Sum,F,Window,Q,Case,When
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
Users = apps.get_model('users', 'CustomUser')
Profile = apps.get_model('profiles', 'Profile')
#channel_layer = get_channel_layer()
# Create your views here.


class DetailNovels(APIView):
  #  def dispatch(self, request, *args, **kwargs):
   #         instance = Novel.objects.get(slug=kwargs['slug'])
    #        if request.user.is_authenticated and instance is not None:
     #          object_viewed_signal.send(instance.__class__, instance=instance, request=request)
      #      return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,*args, **kwargs):
            user =request.user.id
            novel = get_object_or_404(Novel.objects.annotate(statuss = Cast('status__status',output_field=CharField())
            ,authors = Cast('author__author',output_field=CharField())
            ,avg = Avg('review__rating'),reviews = Count('review',distinct=True),
            chapters = Count('novel_chapter__id',distinct=True),
            updated = Max('novel_chapter__created_at'),
            #progress = Count(F('novel_chapter'),filter=Q(novel_chapter__is_seen=False),distinct=True),
            #last_chapter = Count('novel_chapter')
            ),slug = kwargs['slug'])
            Novel.update_avg(novel.id,novel.avg)
          #  novel_chapter = NovelChapter.objects.filter(Q(novel = novel)& Q(is_seen=True)).values('title','slug')[:1]
            comment= Comment.objects.filter(novel = novel).annotate(added_b = Cast('added_by__username',output_field=CharField()),
            count_likes = Count('likes',distinct=True),image = Concat(Value('/media/'),'profile__avatar', output_field=CharField()),
            count_reply = Count('reply_comments__id',distinct=True)).order_by('-date_added')
            comment = CommentSerializer(comment, many=True,read_only=True).data
            last_chapter = NovelChapter.objects.filter(Q(user_seens = Case(
                When(user_seens=None, then=None),
                When(user_seens=request.user.id, then='user_seens')

                ))&Q(novel = novel)).last()
            last_chapter = NovelChapterUser(last_chapter).data
            serializer = NovelSerializer(novel)
            data =serializer.data
            data['user'] = Users.objects.filter(Q(id = Case(
                When(id=None, then=None),
                When(id=request.user.id, then='id')))).values('id')
            data['last_chapter'] = last_chapter
            #comment_reply = Reply_Comment.objects.filter(comment = comment).annotate(like = Count('likes'),added_b=Cast('added_by__username',output_field=CharField()),
             #   avatar = Concat(Value('/media/'),'profile__avatar',output_field=CharField())).values()
           # reply_serialier = Comment_ReplySerializer(comment_reply,many=True)
            #print(comment_reply)
            data['first'] = NovelChapter.objects.filter(novel=novel).values('title','slug').first()
            data['comments'] =comment
            #data['reply'] = reply_serialier.data
            return Response(data)


class Ranking(APIView):
        #qs = novel.filter(rank = 1)
       # print(qs.rank)
        #novel.update(rank = novel.ranking)
    def get(self,request):
        lasts = timezone.now() - timedelta(days=10)
        last_month = timezone.now() - timedelta(days=60)
        
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
        ).filter(Q(novel_chapter__created_at__gt = lasts) | Q(comments__date_added__gt= lasts)).order_by('-created')
        serializer4 = WeeklySerializer( weekly,many=True).data[:12]
        completed = Novel.objects.annotate(chapters = Count('novel_chapter__id',distinct=True)
        ).filter(status__status = 'Completed')
        serializer5 = WeeklySerializer(completed,many=True).data[:12]
        chapters = NovelChapter.objects.annotate(novel_title=Cast('novel__title',output_field=CharField()),
            novel_cover = Concat(Value('/media/'),'novel__cover',output_field=CharField()),novel_slug=Cast('novel__slug',output_field=SlugField())).order_by('-created_at')
        serializer6 = NovelChapterSerializer2(chapters,many=True).data[:24]  
        return Response({'posts':serializer,
                         'trends':serializer1,
                         'rated':serializer2,
                         'popular':serializer3,
                         'weekly':serializer4,
                         'completed':serializer5,
                         'chapters':serializer6,
                         })
    #@method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, *args, **kwargs):
        return super(Ranking, self).dispatch(*args, **kwargs)




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
    queryset = Novel.objects.annotate(popular = Count('review')*2+  Count('comments'),reviews = Count('review',distinct=True),chapters = Count('novel_chapter__id',distinct=True),
    comentarios = Count('comments__id',distinct=True),status_name = Cast('status__status',output_field=CharField()),
    updated =Coalesce(Max('novel_chapter__created_at'),'created')
    )
    serializer_class = NovelSerializer0
    pagination_class = FilterPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = NovelFilter
    
    
    
class AdvancedFilter(ListAPIView):
    queryset = Novel.objects.annotate(popular = Count('review')*2+  Count('comments'),reviews = Count('review',distinct=True),
    chapters = Count('novel_chapter__id',distinct=True),
    updated =Coalesce(Max('novel_chapter__created_at'),'created'),
    comentarios = Count('comments__id',distinct=True),status_name = Cast('status__status',output_field=CharField())).order_by('-created')
    serializer_class = NovelSerializer0
    pagination_class = FilterAdvancedPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvaceFilter
          




class PostList(ListAPIView):
    pagination_class = NovelTagPagination
    serializer_class = NovelSerializer0
    filter_backends = [DjangoFilterBackend]
    filterset_class = NovelFilter
    
    def get_queryset(self):
        qs = Novel.objects.annotate(popular = Count('review')*2+  Count('comments'),reviews = Count('review__id',distinct=True),chapters = Count('novel_chapter__id',distinct=True),
    comentarios = Count('comments__id',distinct=True),
    updated =Coalesce(Max('novel_chapter__created_at'),'created')
    
    ,status_name = Cast('status__status',output_field=CharField())).order_by('-popular')
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


class FavoritesProductsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NovelSerializerFav
    pagination_class = LibraryPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = LibraryFilter
    def get_queryset(self):
        user = self.request.user
        qs = get_object_or_404(Library, user=user).products.annotate(
            progress=Coalesce(Max('novel_chapter__number',filter=Q(novel_chapter__user_seens=user)),0)
            ,chapters = Count('novel_chapter__id',distinct=True),
            added = Cast('library_novel__date_added',output_field=CharField()),
            options = Max('library_novel__option', filter=Q(library_novel__option__isnull=False)),
            updated =Coalesce(Max('novel_chapter__created_at'),'created'),)
        return qs


 #   def get(self, request):
  #      user = request.user
   #     qs = get_object_or_404(Library, user=user).products.annotate(
    #        progress=Max('novel_chapter__number',filter=Q(novel_chapter__user_seens=user))
     #       ,chapters = Count('novel_chapter__id',distinct=True))
      #  print(Library.objects.get(user=user).products.all())
       # products = NovelSerializerFav(
        #    qs, context={'request': request}, many=True).data

        #return Response({'profile':products})


class UpdateFavoritesProductsView(APIView):
    """Get product then if product in favorites novels exists remove from that, 
    else add it to favorites novels"""

    permission_classes = (IsAuthenticated,)
        
    def post(self, request, id):
        user = request.user
        product = get_object_or_404(Novel, id=id)
        obj= get_object_or_404(Library, user=user)
        if obj.products.filter(id=id).exists():
            product.book_marked.remove(user)
            obj.products.remove(product)
            
        else:
            obj.products.add(product)
            product.book_marked.add(user)
      #      async_to_sync(channel_layer.group_send)(
       #        "notification_broadcast",
        #       {
         #      'type': 'send_notification',
          #     'message': json.dumps(f'Realised or update chapter {product.title}')
           # }
         #)
        return Response('added') 
    def put(self,request,novel_id):
        user = request.user
        library_user = get_object_or_404(Library,user = user)
        library = LibraryModel.objects.filter(library=library_user)
        library = get_object_or_404(library, novel=novel_id)
        if request.data['option'] in library.option:
           library.option.remove(request.data.get('option'))
        else:
           library.option = CombinedExpression(F('option'), '||', Value([request.data['option']]))
        library.save()
        return Response('library')
        
        
class ChapterView(APIView):
  #  def dispatch(self, request, *args, **kwargs):
   #     instance = Novel.objects.get(id=1)
    #    if request.user.is_authenticated and instance is not None:
     #       object_viewed_signal.send(instance.__class__, instance=instance, request=request)
      #  return super().dispatch(request, *args, **kwargs)
    def get(self,request,*args, **kwargs):
        user = request.user
        novel_chapter = get_object_or_404(NovelChapter.objects.annotate(novel_slug=Cast('novel__slug',output_field=CharField()),novel_title = Cast('novel__title',output_field=CharField()),
            novel_cover = Concat(Value('/media/'),"novel__cover", output_field=CharField())),slug= kwargs['slug'])
        novel = Novel.objects.get(id = novel_chapter.novel_id)
        if user.is_authenticated:
            novel_chapter.user_seens.add(user)
            HistoryNovel.objects.get_or_create(user=user,novel=novel)
        else: 
            pass
        chapter = NovelChapter.objects.filter(novel=novel).values('slug')
        next= chapter.filter(id__gt=novel_chapter.id).first()
        previous = chapter.filter(id__lt=novel_chapter.id).last()
        serializer = NovelChapterSerializer3(novel_chapter).data
        serializer['next']= next
        serializer['previous'] = previous
        return Response(serializer)
    
    
    
        
        
    
   

class NovelLastView(APIView):
    def get(self,request,*args, **kwargs):
        user = request.user
        novel = get_object_or_404(Novel, id=kwargs['id'])
        last_chapter = NovelChapter.objects.filter(Q(user_seens = user)&Q(novel = novel)).values('title','novel')
        return Response(last_chapter)

class UpdatedComment(APIView):
    def put(self, request,*args, **kwargs):
        comment= Comment.objects.get(id=kwargs['id'])
        comment.body = request.data['body']
        comment.save()
        return Response('updated')
        
class CreateComment(APIView):
    permission_classes = (IsAuthenticated,)
    
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
    def delete(self, request,*args, **kwargs):
        comment = get_object_or_404(Comment, id = kwargs['id'])
        comment.delete()
        return Response('deleted')
    
class CommentView(APIView):
    def get(self , request,*args, **kwargs):
        comment = get_object_or_404(Comment.objects.annotate(count_likes = Count('likes',distinct=True),added_b = Cast('added_by__username',output_field=CharField()),
            image = Concat(Value('/media/'),'profile__avatar',output_field=CharField()), count_reply = Count('reply_comments__id',distinct=True)),id=kwargs['id'])
        serializer = CommentSerializer(comment).data
        comment_reply = Reply_Comment.objects.filter(comment = comment).annotate(like = Count('likes'),added_b=Cast('added_by__username',output_field=CharField()),
               image = Concat(Value('/media/'),'profile__avatar',output_field=CharField()))
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
       serializer2 = WeeklySerializer(novel,many=True).data[:10]
       return Response({'popular':serializer2,'allnovels':serializer})
    
    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, *args, **kwargs):
        return super(SearchNovel, self).dispatch(*args, **kwargs)







