from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Category, Comment
from datetime import timedelta
from django.utils import timezone


class BlogTests(TestCase):

    def setUp(self):
        """Create test data used across multiple tests."""
        # Create an author
        self.user = User.objects.create_user(username='testauthor', password='pass123')

        # Create a category
        self.category = Category.objects.create(name='Django')

        # Create a published post
        self.post = Post.objects.create(
            title="Test Published Post",
            content="This is a test post content.",
            author=self.user,
            status=True,
            published_date=timezone.now()
        )
        self.post.category.add(self.category)

        # Create a draft post (not visible in listings)
        Post.objects.create(
            title="Draft Post",
            content="Should not appear",
            author=self.user,
            status=False
        )

    def test_post_str(self):
        """Test the __str__ method of Post model."""
        self.assertEqual(str(self.post), "Test Published Post")

    def test_category_str(self):
        """Test the __str__ method of Category model."""
        self.assertEqual(str(self.category), "Django")

    def test_comment_str(self):
        """Test the __str__ method of Comment model."""
        comment = Comment.objects.create(
            name="John Doe",
            email="john@example.com",
            subject="Great post!",
            parent_post=self.post,
            approved=True
        )
        self.assertEqual(str(comment), "John Doe")

    def test_blog_home_view(self):
        """Test the main blog home page."""
        response = self.client.get(reverse('blog:blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog-home.html')
        self.assertContains(response, "Test Published Post")
        self.assertNotContains(response, "Draft Post")

    def test_blog_home_pagination(self):
        """Test that pagination works and only shows published posts."""
        # Create more posts to trigger pagination
        for i in range(5):
            Post.objects.create(
                title=f"Extra Post {i}",
                content="Content",
                author=self.user,
                status=True,
                published_date=timezone.now()
            )

        response = self.client.get(reverse('blog:blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context or response.context['post'].has_next())

    def test_blog_single_view(self):
        """Test the single post detail page."""
        response = self.client.get(reverse('blog:blog-single', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog-single.html')
        self.assertContains(response, "Test Published Post")
        self.assertIn('form', response.context)

    def test_blog_single_404_for_draft(self):
        """Unpublished posts should return 404."""
        draft = Post.objects.create(
            title="Secret Draft",
            content="Hidden",
            author=self.user,
            status=False
        )
        response = self.client.get(reverse('blog:blog-single', args=[draft.id]))
        self.assertEqual(response.status_code, 404)

    def test_comment_submission_valid(self):
        """Test submitting a valid comment."""
        comment_data = {
            'parent_post': self.post.id,
            'name': 'Alice',
            'email': 'alice@example.com',
            'subject': 'Nice article!'
        }
        response = self.client.post(
            reverse('blog:blog-single', args=[self.post.id]),
            data=comment_data
        )
        self.assertRedirects(response, reverse('blog:blog-single', args=[self.post.id]))

        # Check comment was saved (approved=False by default)
        self.assertTrue(Comment.objects.filter(name='Alice', parent_post=self.post).exists())
        
        # Check success message
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), "Comment has been sent for approval")

    def test_comment_submission_invalid(self):
        """Test submitting invalid comment (missing required fields)."""
        invalid_data = {
            'name': '',  # Required field empty
            'email': 'invalid',
            'subject': ''
        }
        response = self.client.post(
            reverse('blog:blog-single', args=[self.post.id]),
            data=invalid_data
        )
        self.assertEqual(response.status_code, 200)  # Stays on same page
        self.assertContains(response, "Opps somthing went wrong!")

    def test_category_filter(self):
        """Test filtering posts by category."""
        response = self.client.get(reverse('blog:cat_link', args=['Django']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Published Post")

        response = self.client.get(reverse('blog:cat_link', args=['NonExistent']))
        self.assertEqual(response.status_code, 404)

    def test_author_filter(self):
        """Test filtering posts by author username."""
        response = self.client.get(reverse('blog:author_name', args=['testauthor']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Published Post")

    def test_search_view(self):
        """Test search functionality."""
        response = self.client.get(reverse('blog:search') + '?s=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Published Post")

        response = self.client.get(reverse('blog:search') + '?s=NonMatchingText')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Published Post")|F
