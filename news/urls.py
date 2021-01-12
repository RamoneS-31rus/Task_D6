from django.urls import path
from.views import PostList, PostDetail, PostCreateView, PostUpdateView, PostDeleteView, PostSearch, SearchDetail


urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view()),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('search/', PostSearch.as_view(), name='search'),
    path('search/<int:pk>', SearchDetail.as_view(), name= 'search_detail'),

]