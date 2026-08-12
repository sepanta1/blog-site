from django.urls import path
from rest_framework.routers import SimpleRouter
from .api_views import  UserViewSet, PostViewSet
# urlpatterns = [
#     # api v1
#     path("", PostList.as_view(), name="post_list"),
#     path("<int:pk>/", PostDetail.as_view(), name="post_detail"),
#     path("users/",UserList.as_view()),
#     path("users/<int:pk>/",PostDetail.as_view()),
    
# ]
router = SimpleRouter()
router.register("users", UserViewSet, basename="users")
router.register("", PostViewSet, basename="posts")
urlpatterns = router.urls