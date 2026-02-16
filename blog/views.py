from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
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
    """
    Checks for the owner
    """

    owner_field = "author"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if getattr(obj, self.owner_field) != self.request.user:
            raise PermissionDenied("You do not own this object.")

        return obj


class BlogList(ListView):
    model = Post
    template_name = "blog/blog-home.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.all()
        # url kwargs
        cat_name = self.kwargs.get("cat_name")
        author_name = self.kwargs.get("author_name")
        my_posts = self.kwargs.get("my_posts")
        my_drafts = self.kwargs.get("my_drafts")

        # conditional querysets
        if not (my_posts or my_drafts):
            queryset = queryset.filter(status=True)
        if cat_name:
            queryset = queryset.filter(category__name=cat_name)
        if author_name:
            queryset = queryset.filter(author__username=author_name)
        if my_posts or my_drafts:
            if not self.request.user.is_authenticated:
                raise Http404()
            queryset = queryset.filter(author=self.request.user)

            if my_drafts:
                queryset = queryset.filter(status=False)
            else:
                queryset = queryset.filter(status=True)

        if not queryset.exists():
            raise Http404("No posts found")

        return queryset


class BlogDetail(DetailView):
    model = Post
    template_name = "blog/blog-single.html"
    context_object_name = "post"
    pk_url_kwarg = "pid"

    def get_queryset(self):
        return Post.objects.filter(status=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["comments"] = Comment.objects.filter(
            parent_post=self.object, parent__isnull=True, approved=True
        )

        context["next_post"] = (
            Post.objects.filter(status=True, pk__gt=self.object.pk)
            .order_by("pk")
            .first()
        )

        context["prev_post"] = (
            Post.objects.filter(status=True, pk__lt=self.object.pk)
            .order_by("-pk")
            .first()
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


class BlogSearch(ListView):
    model = Post
    template_name = "blog/blog-home.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(status=True)
        search_term = self.request.GET.get("s")

        if search_term:
            queryset = queryset.filter(title__icontains=search_term)

        return queryset


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


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    template_name = "blog/post-form.html"
    form_class = PostForm
    success_url = reverse_lazy("blog:blog-home")
    success_message = "Post created successfully!"

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class PostUpdateView(
    LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Post
    template_name = "blog/update-post.html"
    form_class = PostForm
    success_url = reverse_lazy("blog:blog-home")
    success_message = "Post updated successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["update_mode"] = True
        return context


class PostDeleteView(
    LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = Post
    template_name = "blog/post-delete.html"
    success_url = reverse_lazy("blog:my-posts")
    success_message = "Post deleted successfully."
