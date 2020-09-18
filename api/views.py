from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, generics, filters
from rest_framework.generics import get_object_or_404, ListCreateAPIView
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.viewsets import ViewSetMixin
 
from .models import Post, Comment, Group, Follow, User
from .permissions import IsOwnerOrReadOnly 
from .serializers import (
    PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
)

  
class PostViewSet(viewsets.ModelViewSet): 
    queryset = Post.objects.all() 
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('group',)
 
    def perform_create(self, serializer): 
        serializer.save(author=self.request.user)

 
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer 
    permission_classes = [ 
        IsAuthenticatedOrReadOnly, 
        IsOwnerOrReadOnly 
    ]   
 
    def perform_create(self, serializer): 
        post_id = self.kwargs.get('id') 
        get_object_or_404(Post, pk=post_id) 
        serializer.save( 
            author=self.request.user, 
            post_id=post_id 
        ) 
     
    def get_queryset(self): 
        post_id = self.kwargs.get('id') 
        queryset = get_object_or_404(Post, pk=post_id).comments.all()
        return queryset


class GroupViewSet(ViewSetMixin, ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [ 
        IsAuthenticatedOrReadOnly, 
        IsOwnerOrReadOnly 
    ]


class FollowViewSet(ViewSetMixin, ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [ 
        IsAuthenticatedOrReadOnly, 
        IsOwnerOrReadOnly 
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username',]

    def perform_create(self, serializer):
        following = get_object_or_404(
            User,
            username=self.request.POST.get('following')
        )
        serializer.save(user=self.request.user, following=following)
