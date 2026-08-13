from django.urls import path
from rest_framework.routers import SimpleRouter
from .api_views import UserViewSet, PostViewSet

router = SimpleRouter(trailing_slash=True)
router.register("users", UserViewSet, basename="users")
router.register("", PostViewSet, basename="posts")
urlpatterns = router.urls
