from django.urls import path
from .api_views import PostList, PostDetail
urlpatterns = [
    # api v1
    path("<int:pk>/", PostDetail.as_view(), name="post_detail"),
    path("", PostList.as_view(), name="post_list"),
]
