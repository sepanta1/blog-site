from django.shortcuts import render, get_object_or_404
from .models import Post
from django.utils.timesince import timesince
from django.http import Http404
from django.utils.timezone import now


def blog_home(request):
    post = Post.objects.filter(status=True)
    if not post.exists():
        raise Http404("No posts found")
    context = {'post': post, }
    return render(request, 'blog/blog-home.html', context)


def blog_single(request, pid):

    post = get_object_or_404(Post, pk=pid, status=1)

    next_post = Post.objects.filter(status=1, pk__gt=pid).order_by('pk').first()
    prev_post = Post.objects.filter(status=1, pk__lt=pid).order_by('-pk').first()
    context = {'post': post, 'next_post': next_post, 'prev_post': prev_post, }
    return render(request, 'blog/blog-single.html', context)


def category_link(request, cat_name):
    post = Post.objects.filter(status=1).filter(category__name=cat_name)
    context = {'post': post}
    return render(request, 'blog/blog-home.html', context)
