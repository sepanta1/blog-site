from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Category, Comment, Post


class PostModelTest(TestCase):
    """
    Tests Post model fields, relationships, and methods
    """

    def setUp(self):
        """Create common objects for Post tests"""
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.category = Category.objects.create(name="Backend")

        self.post = Post.objects.create(
            author=self.user,
            title="Test Post",
            content="<p>Post content</p>",
            status=True,
            published_date=timezone.now(),
        )
        self.post.category.add(self.category)

    def test_post_str(self):
        """Post __str__ should return the title"""
        self.assertEqual(str(self.post), "Test Post")

    def test_get_absolute_url(self):
        """Post get_absolute_url should return correct URL"""
        url = self.post.get_absolute_url()
        self.assertEqual(url, reverse("blog:blog-single", kwargs={"pid": self.post.id}))


class CommentModelTest(TestCase):
    """
    Tests Comment model relationships and string representation
    """

    def setUp(self):
        self.user = User.objects.create_user(username="commenter", password="password")
        self.post = Post.objects.create(
            author=self.user,
            title="Post for comments",
            content="<p>Content</p>",
        )

        self.comment = Comment.objects.create(
            name="Ali",
            email="ali@example.com",
            message="Nice post!",
            parent_post=self.post,
        )

    def test_comment_str(self):
        """Comment __str__ should return commenter's name"""
        self.assertEqual(str(self.comment), "Ali")

