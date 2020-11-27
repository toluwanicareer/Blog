from django.urls import path
from .views import categoryPost, post_list, post_detail, post_search, tagsPost, new_blog_post, update_view, delete_view

urlpatterns = [
    # path('', NewPostView, name='new'),
    path('post/new/', new_blog_post, name='post_new'),
    path('<slug:post>/update/', update_view, name='update'),
    path('<slug:post>/delete/', delete_view, name='delete'),
    path('', post_list, name='home'),
    # path('post/create/', BlogCreateView.as_view(), name='post_new'),
    path('<slug:post>/', post_detail, name='post_detail'),
    path('tags/<slug:tag>/', tagsPost, name='tag_posts'),
    path('category/<slug:category_slug>/', categoryPost, name='category_posts'),
    path('search/', post_search, name='post_search'),
]