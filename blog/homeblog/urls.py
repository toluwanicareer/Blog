from django.urls import path
from .views import categoryPost, post_list, post_detail, post_search, tagsPost, BlogCreateView

urlpatterns = [
    # path('', NewPostView, name='new'),
    path('post/new/', BlogCreateView.as_view(), name='post_new'),
    path('', post_list, name='home'),
    path('<slug:post>/', post_detail, name='post_detail'),
    path('tags/<slug:tag>/', tagsPost, name='tag_posts'),
    path('category/<slug:category_slug>/', categoryPost, name='category_posts'),
    path('search/', post_search, name='post_search'),
]