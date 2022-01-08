from django.urls import path
from . import views
urlpatterns = [
    path('',views.NotificationNovel.as_view()),
    path('redis', views.TestView.as_view(), name='test-url'),
]
