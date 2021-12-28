from django.urls import path
from . import views
urlpatterns = [
    path('',views.NotificationNovel.as_view())
]
