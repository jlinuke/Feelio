"""Feelio — Screening Admin"""
from django.contrib import admin
from .models import EPDSQuestion, EPDSAnswerOption, EPDSResult


class EPDSAnswerOptionInline(admin.TabularInline):
    model = EPDSAnswerOption
    extra = 4
    max_num = 4


@admin.register(EPDSQuestion)
class EPDSQuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'text_en', 'is_reverse_scored')
    list_editable = ('is_reverse_scored',)
    ordering = ('order',)
    inlines = [EPDSAnswerOptionInline]


@admin.register(EPDSResult)
class EPDSResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'tier', 'completed_at')
    list_filter = ('tier',)
    search_fields = ('user__email',)
    date_hierarchy = 'completed_at'
    readonly_fields = ('user', 'score', 'tier', 'responses', 'completed_at')
