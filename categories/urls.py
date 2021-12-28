from django.urls import path
from . import views

urlpatterns = [
    # List categories
    path('tags/', views.TagView.as_view()),
    path('updates/', views.NovelChapterUpdate.as_view())

]

