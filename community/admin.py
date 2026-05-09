"""Feelio — Community Admin"""
from django.contrib import admin
from .models import ForumCategory, ForumThread, Post, Reaction, FlaggedPost, MSGLocation


@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)


@admin.register(ForumThread)
class ForumThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_pinned', 'is_closed', 'view_count', 'created_at')
    list_filter = ('is_pinned', 'is_closed', 'category')
    search_fields = ('title', 'content', 'author__email')
    date_hierarchy = 'created_at'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread', 'author', 'is_flagged', 'created_at')
    list_filter = ('is_flagged',)
    search_fields = ('content', 'author__email')


@admin.register(FlaggedPost)
class FlaggedPostAdmin(admin.ModelAdmin):
    list_display = ('post', 'flagged_by', 'is_reviewed', 'reviewed_by', 'created_at')
    list_filter = ('is_reviewed',)
    readonly_fields = ('post', 'flagged_by', 'reason', 'created_at')
    actions = ['mark_reviewed']

    @admin.action(description='Mark selected flags as reviewed')
    def mark_reviewed(self, request, queryset):
        queryset.update(is_reviewed=True, reviewed_by=request.user)


@admin.register(MSGLocation)
class MSGLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'district', 'meeting_day', 'meeting_time', 'is_active')
    list_filter = ('province', 'is_active')
    search_fields = ('name', 'district', 'phm_contact_name')
