from django.urls import include, path
from django.conf.urls import url
from . import views
from .views import PostList
urlpatterns = [
  path('library', views.FavoritesProductsView.as_view(), name='library'),
  path('favorites-products/update/<int:id>/',views.UpdateFavoritesProductsView.as_view(), name="update-favorites-products"),
  path('tag/<slug:tag>/', PostList.as_view()),
  path('author/<slug:author>/', PostList.as_view()),
  path('novel_chapter/<slug>/', views.NovelView.as_view()),
  path('single_chapter/<slug>/', views.ChapterView.as_view()),
  path('detail/<slug>/', views.DetailNovels.as_view(), name="detail-novel"),
  path('detail/', views.UpdateRank.as_view(), name="detail-novel"),
  path('ranking/', views.Ranking.as_view()),
  path('filter/', views.Filter.as_view()),
  path('postreview/<slug>/', views.CreateReview.as_view()),
  path('putreview/<int:review_id>/', views.CreateReview.as_view()),
  path('postcomment/<id>/', views.CreateComment.as_view()),
  path('comment/<id>/', views.CommentView.as_view()),
  path('allnovels/', views.SearchNovel.as_view()),
  path('advancedfilter/',views.AdvancedFilter.as_view())




]