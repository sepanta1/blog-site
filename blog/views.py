from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Post, Comments
from .forms import Comments_form
from django.contrib import messages
from django.utils.timesince import timesince
from django.http import Http404
from django.utils.timezone import now


def blog_home(request, cat_name=None, author_name=None):
    """
    Displays the main blog home page with a list of published posts.
    Supports optional filtering by category or author.
    Posts are paginated (2 per page).
    """
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
    """
    Renders the detail page for a single blog post.
    Shows the post, approved comments, previous/next post links,
    and handles new comment submission.
    """
    post = get_object_or_404(Post, pk=pid, status=1)
    comments = Comments.objects.filter(parent_post=post.id, approved=True)
    if request.method == "POST":
        form = Comments_form(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Comment has been sent for approval")
            return redirect("blog:blog-single", pid=post.pk)
        else:
            messages.add_message(request, messages.ERROR,
                                 "Opps somthing went wrong!")
    form = Comments_form()
    next_post = Post.objects.filter(
        status=1, pk__gt=pid).order_by('pk').first()
    prev_post = Post.objects.filter(
        status=1, pk__lt=pid).order_by('-pk').first()
    context = {'post': post, 'next_post': next_post,
               'prev_post': prev_post, 'comments': comments, 'form': form}
    return render(request, 'blog/blog-single.html', context)


def blog_category(request, cat_name):
    """
    Displays a list of published posts belonging to a specific category.
    Reuses the same template as the blog home page.
    """
    post = Post.objects.filter(status=1).filter(category__name=cat_name)
    context = {'post': post}
    return render(request, 'blog/blog-home.html', context)


def blog_search(request):
    """
    Handles search functionality.
    Filters published posts by content containing the search term (case-insensitive).
    """
    post = Post.objects.filter(status=1)
    if request.method == 'GET':
        post = post.filter(content__icontains=request.GET.get('s'))
    context = {'post': post}
    return render(request, 'blog/blog-home.html', context)
