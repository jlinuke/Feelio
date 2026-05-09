"""Feelio — Accounts Admin"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('email', 'first_name', 'is_anonymous_mode', 'language_preference', 'date_joined', 'is_active')
    list_filter = ('is_anonymous_mode', 'language_preference', 'is_active')
    search_fields = ('email', 'first_name', 'display_alias')
    ordering = ('-date_joined',)
    fieldsets = UserAdmin.fieldsets + (
        ('Feelio', {'fields': ('phone', 'display_alias', 'is_anonymous_mode', 'language_preference')}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'province', 'district', 'is_first_time_mother', 'share_data_for_research')
    list_filter = ('province', 'is_first_time_mother')
    search_fields = ('user__email', 'district')
