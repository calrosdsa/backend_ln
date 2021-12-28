from django.db.models.expressions import Value
from django.db.models.fields import CharField, SlugField
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import generic
#Auth dependencies
from rest_framework.decorators import api_view, permission_classes #for authenticated routes
from rest_framework.permissions import IsAuthenticated #for authenticated routes
from django.views.decorators.csrf import csrf_exempt #for authenticated routes
# API dependencies
from .serializers import CommentSerializerUser, ProfileSerializer,HistorySerializer, ReviewSerialiezerUser
from .models import History, Profile
from rest_framework import pagination, serializers, status
import json #Useful for POST and PUT requests
from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps 
from rest_framework.response import Response
from rest_framework.views import APIView
from novels.models import Comment, Review
from django.db.models import Count
from django.db.models.functions import Cast, Concat
from rest_framework.generics import ListAPIView,RetrieveAPIView,CreateAPIView


Users = apps.get_model('users', 'CustomUser')


class ReviewUserView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self,request):
        user = request.user
        review = Review.objects.filter(added_by=user).annotate(like =Count('likes',distinct=True),avatar = Concat(Value('/media/'),'profile__avatar',output_field=CharField()),
            user = Cast('added_by__username',output_field=CharField()),novel_title = Cast('novel__title',output_field=CharField()),
            novel_cover=Concat(Value('/media/'),'novel__cover',output_field=CharField()),novel_slug= Cast('novel__slug',output_field=SlugField()))
        serializer = ReviewSerialiezerUser(review,many=True).data
        return Response({'reviews':serializer})

class CommentUserView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        user =request.user
        comment = Comment.objects.filter(added_by = user).annotate(count_likes = Count('likes'),added_b = Cast('added_by__username',output_field=CharField()),
            image = Concat(Value('/media/'),'profile__avatar',output_field=CharField()),
            count_reply = Count('reply_comments',distinct=True),novel_title = Cast('novel__title',output_field=CharField()),
            novel_cover = Concat(Value('/media/'),'novel__cover',output_field=CharField()),novel_slug=Cast('novel__slug',output_field=SlugField()))
        serializer = CommentSerializerUser(comment, many=True).data
        return Response({'comments':serializer})
    
# Create your views here.

# // @route GET profile/members
# // @desc Get all profiles using
# // @access Public (No Authentication)
class HistoryView(ListAPIView):
    serializer_class = HistorySerializer
    queryset=History.objects.all()
    pagination_class = None
    def list(self, request, *args, **kwargs):
        user=request.user
        queryset = self.get_queryset()
        history = queryset.filter(user=user)
        serializer = HistorySerializer(history,many=True)
        return Response(serializer.data)
    #def get_queryset(self):
    #    queryset = super(History,self).get_queryset()
     #   user = self.kwargs.get('user')
      #  user_only= queryset.filter(user=user)
       # return user_only





class ProfileView(ListAPIView):
    permission_classes =[IsAuthenticated,]
    queryset = Profile.objects.all()
    def list(self,request):
        user = request.user
        try:
           profile = Profile.objects.get(user=user.id)
           serializer = serializer = ProfileSerializer(profile)
           data = serializer.data
           return Response(data)
        except ObjectDoesNotExist:
           return JsonResponse({'msg': 'There is no profile found.' }, safe=False, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST','DELETE'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def create_delete_profile(request):
    user=Users.objects.get(id=request.user.id)
    print(request.user)
    print('this worked')
    print(request.data)

    if request.method == 'POST':
        try:
            profile= Profile.objects.get(user=user)
            profile.bio = request.data['bio']
            profile.name = request.data['name']
            if request.data['avatar'] == '':
                profile.avatar
            else:
                profile.avatar = request.data['avatar']
            profile.save()
            serializers = ProfileSerializer(profile)
            data = serializers.data
            data['user'] = user.username
            return JsonResponse({'profile': data},safe=False,status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            profile=Profile.objects.update_or_create(
                user=user,
                name=request.data['name'],
                bio=request.data['bio'],
                avatar=request.data['avatar']
            )
            serializer= serializer = ProfileSerializer(profile)
            data= serializer.data
            data['user']= user.username
            return JsonResponse({'profile': data}, safe=False, status=status.HTTP_201_CREATED)
        except Exception:
                  return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'detail': 'User account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



