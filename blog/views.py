from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post

from django.utils.timesince import timesince
from django.http import Http404
from django.utils.timezone import now


def blog_home(request, cat_name=None, author_name=None):
    post = Post.objects.filter(status=True).order_by('-published_date')
    if cat_name:
        post = post.filter(
            category__name=cat_name)
    if author_name:
        post = post.filter(
            author__username=author_name)
    if not post.exists():
        raise Http404("No posts found")
    p = Paginator(post, 2)
    page_number = request.GET.get('page')
    post = p.get_page(page_number)  # returns the desired page object

    context = {'post': post}
    return render(request, 'blog/blog-home.html', context)


def blog_single(request, pid):

    post = get_object_or_404(Post, pk=pid, status=1)

    next_post = Post.objects.filter(
        status=1, pk__gt=pid).order_by('pk').first()
    prev_post = Post.objects.filter(
        status=1, pk__lt=pid).order_by('-pk').first()
    context = {'post': post, 'next_post': next_post, 'prev_post': prev_post, }
    return render(request, 'blog/blog-single.html', context)


def blog_category(request, cat_name):
    post = Post.objects.filter(status=1).filter(category__name=cat_name)
    context = {'post': post}
    return render(request, 'blog/blog-home.html', context)


def blog_search(request):
    post = Post.objects.filter(status=1)
    if request.method == 'GET':
        post = post.filter(content__icontains=request.GET.get('s'))
    context = {'post': post}
    return render(request, 'blog/blog-home.html', context)


def test(request):
    pass
    # if request.method == 'POST':
    #     form = Contact_form(request.POST)
    #     if form.is_valid():
            
    #         form.save()

    # else:
    #     form = Contact_form()
    # return render(request, 'test.html', {'form': form})
