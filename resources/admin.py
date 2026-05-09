"""Feelio — Resources Admin"""
from django.contrib import admin
from .models import Helpline, Article, PHMContact


@admin.register(Helpline)
class HelplineAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'available_hours', 'languages', 'is_featured', 'order')
    list_editable = ('is_featured', 'order')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'created_at')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published',)


@admin.register(PHMContact)
class PHMContactAdmin(admin.ModelAdmin):
    list_display = ('district', 'province', 'moh_office', 'phone', 'is_active')
    list_filter = ('province', 'is_active')
    search_fields = ('district', 'moh_office', 'name')
