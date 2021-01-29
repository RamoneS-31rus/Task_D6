from django.urls import path
from.views import PostList, PostDetail, PostCreateView, PostUpdateView, PostDeleteView, PostSearch


urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('news/<int:pk>', PostDetail.as_view(), name='post'),
    path('news/add/', PostCreateView.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('news/search/', PostSearch.as_view(), name='search'),

]