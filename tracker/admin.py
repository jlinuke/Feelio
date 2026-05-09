"""Feelio — Tracker Admin"""
from django.contrib import admin
from .models import MoodEntry, JournalEntry, SymptomTag


@admin.register(SymptomTag)
class SymptomTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'mood_score', 'one_word_feeling', 'created_at')
    list_filter = ('mood_score', 'date')
    search_fields = ('user__email', 'one_word_feeling')
    date_hierarchy = 'date'


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_pinned', 'created_at')
    list_filter = ('is_pinned',)
    search_fields = ('user__email', 'title', 'content')
