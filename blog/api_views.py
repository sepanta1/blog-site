from rest_framework import generics
from .permissions import IsAuthorOrReadOnly
from .models import Post
from .serializers import PostSerializer

class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAuthorOrReadOnly,) 
    queryset = Post.objects.filter(status=True) 
    serializer_class = PostSerializer
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,) 
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    