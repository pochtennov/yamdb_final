from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .custom_mixins import CreateDelListViewSet
from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorOrModeratorOrAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          CreateUserSerializer, GenreSerializer,
                          ObtainTokenSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleGetSerializer,
                          UserSerializer)

User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def create_user(request):
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create(
            email=email, is_active=False, username=email)

    token = default_token_generator.make_token(user)

    send_mail(
        'Your registration token',
        f'Your token: {token}',
        settings.SENDER_EMAIL_ADDRESS,
        [email],
        fail_silently=False,
    )
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def obtain_token(request):
    serializer = ObtainTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    is_accepted = default_token_generator.check_token(
        user, confirmation_code)
    if is_accepted:
        user.is_active = True
        user.save()
        refresh = RefreshToken.for_user(user)
        data = {'access': str(refresh.access_token)}
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)

    @action(
        methods=['get', 'patch'],
        detail=False, permission_classes=[IsAuthenticated]
    )
    def me(self, request, *args, **kwargs):
        user = request.user
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            # rewrite role so user can't change his role
            serializer.save(role=user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CreateDelListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly
    )
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination


class GenreViewSet(CreateDelListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly
    )
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleGetSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly
    )
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_queryset(self):
        return Title.objects.order_by('name').annotate(
            rating=Coalesce(Avg('reviews__score'), None))

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitleCreateSerializer
        return TitleGetSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdminOrReadOnly
    )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs.get("title_id"),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs.get("title_id"),
        )
        serializer.save(review=review, author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdminOrReadOnly
    )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title, id=self.kwargs.get("title_id")
        )
        serializer.save(title=title, author=self.request.user)
