from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
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
    title = models.CharField(max_length=50, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True)
    thumbnail = models.ImageField(upload_to='images/', blank=True, null=False)
    body = HTMLField(null=False, blank=True)
    photos = models.ImageField(upload_to='photos/', blank=True, null=False)
    summary = models.TextField(null=False, blank=True)
    slug = models.SlugField(max_length=250, unique_for_date='publish', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    meta_title = models.CharField(max_length=50, blank=True)
    meta_description = models.TextField(null=False, blank=True)
    keywords = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', blank=True)
    featured = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ('-publish',)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',
            args=[self.slug])



    