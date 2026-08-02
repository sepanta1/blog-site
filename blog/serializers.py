from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "author",
            "title",
            "body",
            "created_at",
            )
        model = Post
# blog/serializers.py
from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer

from .models import Post


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    category = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Post._meta.get_field("category").related_model.objects.all()
    )
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "image",
            "author",
            "title",
            "content",
            "tags",
            "category",
            "counted_views",
            "status",
            "published_date",
            "created_date",
        )
        read_only_fields = ("counted_views", "created_date")