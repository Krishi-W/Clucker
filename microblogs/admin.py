"""Configuration of the admin interface for microblogs"""
from django.contrib import admin

from microblogs.models import Post, User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users"""
    list_display = [
        'username', 'first_name', 'last_name', 'email', 'is_active',
    ]

@admin.register(Post)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for posts"""
    list_display = [
        'author', 'text', 'created_at',
    ]
