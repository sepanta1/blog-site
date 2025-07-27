from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    # image =
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)

    title = models.CharField(max_length=255)
    content = models.TextField()
    # tags =
    # category =
    counted_views = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

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
# Create your models here.
