from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
 
from django.urls import path, include 
 
from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet


router_v1 = routers.DefaultRouter()
router_v1.register(r'follow', FollowViewSet, basename='Follow')
router_v1.register(r'group', GroupViewSet, basename='Group')
router_v1.register(r'posts', PostViewSet, basename='Posts') 
router_v1.register(
    r'posts/(?P<id>\d+)/comments',
    CommentViewSet,
    basename='Comment' 
) 
 
urlpatterns = [
    path('', include(router_v1.urls)), 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 
