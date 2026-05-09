"""Feelio — Dashboard Admin"""
from django.contrib import admin
from .models import DailyAffirmation, CheckInStreak


@admin.register(DailyAffirmation)
class DailyAffirmationAdmin(admin.ModelAdmin):
    list_display = ('text_en', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('text_en',)


@admin.register(CheckInStreak)
class CheckInStreakAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_streak', 'longest_streak', 'last_checkin_date')
    search_fields = ('user__email',)
    readonly_fields = ('user', 'current_streak', 'longest_streak', 'last_checkin_date')
