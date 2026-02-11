from django import forms

from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "message"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "image",
            "title",
            "content",
            "tags",
            "category",
            "status",
            "published_date",
        ]

        widgets = {
            "published_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
