from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("blog-home/", views.BlogList.as_view(), name="blog-home"),
    path("category/<str:cat_name>", views.BlogList.as_view(), name="cat_link"),
    path("author/<str:author_name>", views.BlogList.as_view(), name="author_name"),
    path("myposts/", views.BlogList.as_view(), {"my_posts": True}, name="my-posts"),
    path("mydrafts/", views.BlogList.as_view(), {"my_drafts": True}, name="my-drafts"),
    path("<int:pid>/", views.BlogDetail.as_view(), name="blog-single"),
    path("search/", views.BlogSearch.as_view(), name="search"),
    path("posts/create/", views.PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"),
    path("posts/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
    path(
        "post/<int:post_id>/comment/",
        views.CommentCreateView.as_view(),
        name="comment-create",
    ),
]
