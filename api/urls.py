from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import (
    CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet, TitleViewSet,
    UsersViewSet,
)

router_v1 = DefaultRouter()

router_v1.register(r'users', UsersViewSet)
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'titles', TitleViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/email', views.create_user, name='create_user'),
    path('v1/auth/token', views.obtain_token, name='obtain_token'),
]
