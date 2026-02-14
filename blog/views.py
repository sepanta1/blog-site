from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post


class OwnerRequiredMixin:
    owner_field = "author"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if getattr(obj, self.owner_field) != self.request.user:
            raise PermissionDenied("You do not own this object.")

        return obj


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        form.instance.parent_post = post

        parent_id = self.kwargs.get("parent_id")
        if parent_id:
            form.instance.parent = get_object_or_404(Comment, pk=parent_id)

        return super().form_valid(form)

    def get_success_url(self):
        return self.object.parent_post.get_absolute_url()


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post-form.html"
    form_class = PostForm
    success_url = reverse_lazy("blog:blog-home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class PostUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Post
    template_name = "blog/update-post.html"
    form_class = PostForm
    success_url = reverse_lazy("blog:blog-home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["update_mode"] = True
        return context


class PostDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Post


class MyPosts(ListView, LoginRequiredMixin, OwnerRequiredMixin):
    model = Post
    template_name = "blog/blog-home.html"
    context_object_name = "post"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class BlogList(ListView):
    model = Post
    template_name = "blog/blog-home.html"
    context_object_name = "post"
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(status=True)

        cat_name = self.kwargs.get("cat_name")
        author_name = self.kwargs.get("author_name")

        if cat_name:
            queryset = queryset.filter(category__name=cat_name)
        if author_name:
            queryset = queryset.filter(author__username=author_name)
        if not queryset.exists():
            raise Http404("No posts found")
        return queryset


class BlogDetail(DetailView):
    model = Post
    template_name = "blog/blog-single.html"
    context_object_name = "post"
    pk_url_kwarg = "pid"

    def get_queryset(self):
        return Post.objects.filter(status=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["comments"] = Comment.objects.filter(
            parent_post=self.object, parent__isnull=True, approved=True
        )

        context["next_post"] = (
            Post.objects.filter(status=1, pk__gt=self.object.pk).order_by("pk").first()
        )

        context["prev_post"] = (
            Post.objects.filter(status=1, pk__lt=self.object.pk).order_by("-pk").first()
        )

        context["form"] = CommentForm()

        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        Post.objects.filter(pk=obj.pk).update(counted_views=F("counted_views") + 1)

        obj.refresh_from_db()

        return obj

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.parent_post = self.get_object()

            parent_id = request.POST.get("parent_id")
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)

            comment.save()
            messages.success(request, "Comment has been sent for approval")
            return redirect("blog:blog-single", pid=self.kwargs["pid"])
        else:
            messages.error(request, "Oops something went wrong!")

            context = self.get_context_data()
            context["form"] = form
            return self.render_to_response(context)


def blog_category(request, cat_name):
    """
    Displays a list of published posts belonging to a specific category.
    """
    post = Post.objects.filter(status=1).filter(category__name=cat_name)
    context = {"post": post}
    return render(request, "blog/blog-home.html", context)


def blog_search(request):
    """
    Handles search functionality.
    """
    post = Post.objects.filter(status=1)
    search_term = request.GET.get("s")

    if request.method == "GET":
        post = post.filter(title__icontains=search_term)

    context = {"post": post}
    return render(request, "blog/blog-home.html", context)


# def blog_single(request, pid):
#     post = get_object_or_404(Post, pk=pid, status=1)

#     comments = Comment.objects.filter(
#         parent_post=post, parent__isnull=True, approved=True
#     )

#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.parent_post = post

#             parent_id = request.POST.get("parent_id")
#             if parent_id:
#                 comment.parent = Comment.objects.get(id=parent_id)

#             comment.save()

#             messages.success(request, "Comment has been sent for approval")
#             return redirect("blog:blog-single", pid=post.pk)
#         else:
#             messages.error(request, "Oops something went wrong!")

#     form = CommentForm()

#     next_post = Post.objects.filter(status=1, pk__gt=pid).order_by("pk").first()
#     prev_post = Post.objects.filter(status=1, pk__lt=pid).order_by("-pk").first()

#     context = {
#         "post": post,
#         "next_post": next_post,
#         "prev_post": prev_post,
#         "comments": comments,
#         "form": form,
#     }
#     return render(request, "blog/blog-single.html", context)


# def blog_home(request, cat_name=None, author_name=None):
#     """
#     Displays the main blog home page with a list of published posts.
#     Supports optional filtering by category or author.
#     """
#     post = Post.objects.filter(status=True).order_by("-published_date")
#     if cat_name:
#         post = post.filter(category__name=cat_name)
#     if author_name:
#         post = post.filter(author__username=author_name)
#     if not post.exists():
#         raise Http404("No posts found")
#     p = Paginator(post, 2)
#     page_number = request.GET.get("page")
#     post = p.get_page(page_number)  # returns the desired page object


#     context = {"post": post}
#     return render(request, "blog/blog-home.html", context)
