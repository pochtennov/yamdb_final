from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Category, Comment, Genre, Review, Title, User


class CustomUserAdmin(BaseUserAdmin):
    ordering = ('pk', 'email')
    list_display = (
        'pk',
        'email',
        'username',
        'first_name',
        'last_name',
        'role',
        'bio'
    )
    search_fields = ('pk', 'email', 'username', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'bio')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'role', 'user_permissions',)})
    )
    list_filter = ('email', 'username')
    empty_value_display = '-nothing-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'score', 'pub_date')
    search_fields = ('text', 'author')
    list_filter = ('pub_date', )
    empty_value_display = '-nothing-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'review', 'pub_date')
    search_fields = ('text', 'author')
    list_filter = ('pub_date', )
    empty_value_display = '-nothing-'


admin.site.register(User, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
