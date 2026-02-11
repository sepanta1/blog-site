from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from tinymce.models import HTMLField


# Abstract models avoiding DRY
class TimeStampedModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Postable(models.Model):
    message = models.TextField(max_length=500)

    class Meta:
        abstract = True


class Category(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(TimeStampedModel):

    image = models.ImageField(
        upload_to="blog/", default="blog/default.webp", null=True, blank=True
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    title = models.CharField(max_length=255)
    content = HTMLField()
    tags = TaggableManager()
    category = models.ManyToManyField(Category, default=None)
    counted_views = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:blog-single", kwargs={"pid": self.id})

    class Meta:
        get_latest_by = "created_date"


class Contact(TimeStampedModel, Postable):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)

    class Meta:
        get_latest_by = "created_date"


class Comment(TimeStampedModel, Postable):

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    approved = models.BooleanField(default=True)
    parent_post = models.ForeignKey("Post", on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    class Meta:
        get_latest_by = "created_date"

    def __str__(self):
        return self.name
