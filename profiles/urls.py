from django.urls import include, path
from . import views

urlpatterns = [
  path('', views.create_delete_profile),
  path('me', views.ProfileView.as_view()),
  path('detail/', views.HistoryView.as_view(), name="detail-novel"),
  path('review/', views.ReviewUserView.as_view(), name="detail-novel"),
  path('comment/', views.CommentUserView.as_view(), name="detail-novel"),


  
]
