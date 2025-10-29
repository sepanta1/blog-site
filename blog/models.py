from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.urls import reverse
from tinymce.models import HTMLField
class Category(models.Model):
    name= models.CharField(max_length=50)
    def __str__(self):
        return self.name
class Post(models.Model):
    image =models.ImageField(upload_to='blog/',default='blog/default.jpg',null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    title = models.CharField(max_length=255)
    content = HTMLField()
    tags =TaggableManager()
    category =models.ManyToManyField(Category, default=None)
    counted_views = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("blog:blog-single", kwargs={"pid": self.id})
    class Meta:
        get_latest_by = 'created_date'
    
    


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created_date'
        
class Comments(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField(blank=True, null=True)
    subject=models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    approved=models.BooleanField(default=False)
    parent_post=models.ForeignKey("Post", on_delete=models.CASCADE)
   
    
    class Meta:
        get_latest_by='created_date'
    def __str__(self):
        return self.name
    