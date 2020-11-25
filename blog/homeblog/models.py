from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from tinymce.models import HTMLField


class Category(models.Model):
    
    
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',
            args=[self.title, self.created_at, self.slug])

    class Meta:
        verbose_name_plural = "Categories"




class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=50)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    body = HTMLField(null=False, blank=False)
    thumbnail = models.ImageField(upload_to='images/')
    summary = models.TextField(null=False, blank=False)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    meta_title = models.CharField(max_length=50)
    meta_description = models.TextField(null=False, blank=False)
    keywords = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ('-publish',)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',
            args=[self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


    