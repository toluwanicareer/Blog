from django.urls.base import reverse, reverse_lazy
from .models import Category, Post
from django.shortcuts import render, get_object_or_404, redirect
from .forms import SearchForm, PostForm
from taggit.models import Tag
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
import pdb
from django.contrib.auth.decorators import login_required


def post_list(request,  tag_slug=None):
    object_list = Post.objects.filter(status='published')
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
    featured_post = Post.objects.filter(featured=True).order_by('-publish')[0:4]
    latest_posts = Post.objects.filter(status='published').order_by('-publish')[0:4]
   
   
    return render(request, 'blog.html', {'page':page, 
        'posts': posts, 
        'category': category, 
        'featured_post': featured_post,
        'latest_posts': latest_posts,
    })

def post_detail(request, post):
    post = get_object_or_404(Post, slug=post,
        status='published',
        )

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    category = Category.objects.all()
    featured_post = Post.objects.filter(featured=True).order_by('-publish')[0:4]
    tags = post.tags.names()
    latest_posts = Post.objects.filter(status='published').order_by('-publish')[0:4]
    

    return render(request, 'blog-details.html', {'post': post, 
        'similar_posts': similar_posts,
        'category':category,
        'featured_post': featured_post,
        'featured_tags':tags,
        'latest_posts': latest_posts,
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
            ).filter(rank__gte=0.3).order_by('-created_at')

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


@login_required
def new_blog_post(request):
    blog = Post.objects.all()
    new_post = None
    if request.method == 'POST':
        # A post was posted
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            # Create post object but don't save to database yet
            new_post = post_form.save(commit=False)
            # Save the post to the database
            new_post.save()
            return redirect('/')
    else:
        post_form = PostForm()

    return render(request, 'post_new.html', {'blog': blog,
    'new_post': new_post, 'post_form': post_form})


@login_required
def update_view(request, post):
    instance = get_object_or_404(Post, slug = post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            success_url = redirect('/')
            return success_url
    else:
        form = PostForm(instance=instance)
    return render(request, 'update_view.html', {'form':form})


@login_required
def delete_view(request, post):
    context ={}
    instance = get_object_or_404(Post, slug = post)
    if request.method == 'POST':
        instance.delete()
        success_url = redirect('/')
        return success_url
    return render(request, 'delete_view.html', context)

