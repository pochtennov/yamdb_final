from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .managers import UserManager
from .validators import custom_year_validator


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        USER = 'user', 'user'
        MODERATOR = 'moderator', 'moderator'
        ADMIN = 'admin', 'admin'

    username = models.CharField(
        unique=True, max_length=30, blank=False, verbose_name='username')
    email = models.EmailField(unique=True, verbose_name='email', blank=False)
    bio = models.TextField(max_length=200, verbose_name='bio', blank=True)
    role = models.CharField(
        max_length=30,
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
        verbose_name='role')

    @property
    def is_admin(self):
        return self.role == self.RoleChoices.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.RoleChoices.MODERATOR

    def set_admin(self):
        self.role = self.RoleChoices.ADMIN

    def set_moderator(self):
        self.role = self.RoleChoices.MODERATOR

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('username',)

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            db_index=True, verbose_name='name')
    slug = models.SlugField(unique=True, blank=True, verbose_name='slug')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            db_index=True, verbose_name='name')
    slug = models.SlugField(unique=True, verbose_name='slug')

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name='name'
    )
    description = models.TextField(
        blank=True, null=True, verbose_name='description'
    )
    year = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='year',
        validators=(
            custom_year_validator,
        ))
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='category'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name='genre'
    )

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='author')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='title')
    text = models.TextField(verbose_name='text')
    score = models.PositiveSmallIntegerField(
        verbose_name='score', validators=[
            MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True,
    )

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='only one review for one author',
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='author')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='review')
    text = models.TextField(verbose_name='text')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True,
    )

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
