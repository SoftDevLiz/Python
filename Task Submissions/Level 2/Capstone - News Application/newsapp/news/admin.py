"""
admin.py – Django admin configuration for the News Application.

All models are registered with custom ModelAdmin classes to provide a
useful admin interface for site administrators.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from news.models import Article, CustomUser, Newsletter, Publisher


# ---------------------------------------------------------------------------
# Publisher
# ---------------------------------------------------------------------------
@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'created_at']
    search_fields = ['name']
    ordering = ['name']


# ---------------------------------------------------------------------------
# CustomUser
# ---------------------------------------------------------------------------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Extends Django's built-in UserAdmin so our extra fields appear
    in the admin change form.
    """
    list_display = ['username', 'email', 'role', 'publisher', 'is_staff']
    list_filter = ['role', 'publisher', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    # Add our custom fields to the existing fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('News App Role & Subscriptions', {
            'fields': (
                'role',
                'publisher',
                'subscribed_publishers',
                'subscribed_journalists',
            ),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('News App Role', {
            'fields': ('role', 'email'),
        }),
    )


# ---------------------------------------------------------------------------
# Article
# ---------------------------------------------------------------------------
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publisher', 'approved', 'approved_by', 'created_at']
    list_filter = ['approved', 'publisher', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'approved_at', 'approved_by']
    ordering = ['-created_at']

    def approval_status(self, obj):
        """Display a coloured badge in the list view."""
        if obj.approved:
            return format_html('<span style="color:green;">✓ Approved</span>')
        return format_html('<span style="color:orange;">⏳ Pending</span>')

    approval_status.short_description = 'Status'


# ---------------------------------------------------------------------------
# Newsletter
# ---------------------------------------------------------------------------
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'article_count']
    search_fields = ['title', 'author__username']
    filter_horizontal = ['articles']  # Nice M2M widget
    readonly_fields = ['created_at', 'updated_at']

    def article_count(self, obj):
        return obj.articles.count()

    article_count.short_description = '# Articles'
