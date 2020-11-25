from django.urls import path
from .views import categoryPost, new_blog_post, post_list, post_detail, post_search, tagsPost

urlpatterns = [
    # path('', NewPostView, name='new'),
    path('post/new/', new_blog_post, name='post_new'),
    path('', post_list, name='home'),
    # path('<slug:post>/edit/', BlogUpdateView.as_view(), name='post_edit'),
    path('<slug:post>/', post_detail, name='post_detail'),
    path('tags/<slug:tag>/', tagsPost, name='tag_posts'),
    path('category/<slug:category_slug>/', categoryPost, name='category_posts'),
    path('search/', post_search, name='post_search'),
]