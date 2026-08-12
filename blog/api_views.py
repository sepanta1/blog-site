from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import viewsets
from .permissions import IsAuthorOrReadOnly
from .models import Post
from .serializers import PostSerializer,UserSerializer
from rest_framework.permissions import IsAdminUser
class PostViewSet(viewsets.ModelViewSet):
    permission_classes= [IsAuthorOrReadOnly]
    queryset= Post.objects.all()
    serializer_class= PostSerializer
    
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset= get_user_model().objects.all()
    serializer_class=UserSerializer
    
# class PostList(generics.ListCreateAPIView):
#     permission_classes = (IsAuthorOrReadOnly,) 
#     queryset = Post.objects.filter(status=True) 
#     serializer_class = PostSerializer
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsAuthorOrReadOnly,) 
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
    
# class UserList(generics.ListAPIView):
#     queryset= get_user_model().objects.all()
#     serializer_class= UserSerializer

# class UserDetail(generics.RetrieveUpdateAPIView):
#     queryset= get_user_model().objects.all()
#     serializer_class= UserSerializer

