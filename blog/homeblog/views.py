from .models import Category, Post
from django.shortcuts import render, get_object_or_404
from .forms import CommentForm, SearchForm
from taggit.models import Tag
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
import pdb


def post_list(request,  tag_slug=None):
    object_list = Post.objects.all()
    tag = None
    
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    category = Category.objects.all()
    featured_post = Post.objects.filter(featured=True)
   
   
    return render(request, 'blog.html', {'page':page, 
        'posts': posts, 
        'category':category, 
        'featured_post': featured_post,
        
    })

def post_detail(request, post):
    post = get_object_or_404(Post, slug=post,
        status='published',
        )

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    category = Category.objects.all()
    featured_post = Post.objects.filter(featured=True)
    tags = post.tags.names()
    

    return render(request, 'blog-details.html', {'post': post, 
        'comments': comments, 
        'new_comment': new_comment, 
        'comment_form': comment_form,
        'similar_posts': similar_posts,
        'category':category,
        'featured_post': featured_post,
        'featured_tags':tags,
        })

    
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(
            search=search_vector, rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')

    return render(request,'search.html',
            {'form': form,
            'query': query,
            'results': results
    })



def tagsPost(request, tag):
    object_list = Post.objects.filter(tags__name__in=[tag]).distinct()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    category = Category.objects.all()
    featured_post = Post.objects.filter(featured=True)
    return render(request, 'blog.html', {'page':page, 
        'posts': posts, 
        'category':category, 
        'featured_post': featured_post,
        
    })


def categoryPost(request, category_slug):
    object_list = Post.objects.filter(category__slug=category_slug)
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    category = Category.objects.all()
    featured_post = Post.objects.filter(featured=True)
    return render(request, 'blog.html', {'page':page, 
        'posts': posts, 
        'category':category, 
        'featured_post': featured_post,
        
    })
