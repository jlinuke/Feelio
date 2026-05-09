"""Feelio — Screening App Models: EPDS"""
from django.db import models
from django.conf import settings


class EPDSQuestion(models.Model):
    """The 10 standard EPDS questions."""
    order = models.PositiveSmallIntegerField(unique=True)
    text_en = models.TextField()
    text_si = models.TextField(blank=True)
    text_ta = models.TextField(blank=True)
    is_reverse_scored = models.BooleanField(default=False, help_text="Questions 3,5,6,7,8,9,10 use reverse scoring")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Q{self.order}: {self.text_en[:60]}..."


class EPDSAnswerOption(models.Model):
    """4 answer options per question."""
    question = models.ForeignKey(EPDSQuestion, on_delete=models.CASCADE, related_name='options')
    text_en = models.CharField(max_length=120)
    text_si = models.CharField(max_length=120, blank=True)
    text_ta = models.CharField(max_length=120, blank=True)
    score_value = models.PositiveSmallIntegerField()  # 0, 1, 2, or 3

    class Meta:
        ordering = ['score_value']

    def __str__(self):
        return f"Q{self.question.order} — {self.text_en} ({self.score_value})"


class EPDSResult(models.Model):
    """Completed screening session."""
    TIER_DOING_WELL = 'doing_well'
    TIER_NEEDS_ATTENTION = 'needs_attention'
    TIER_SEEK_SUPPORT = 'seek_support'

    TIER_CHOICES = [
        (TIER_DOING_WELL, 'Doing Well'),
        (TIER_NEEDS_ATTENTION, 'Needs Attention'),
        (TIER_SEEK_SUPPORT, 'Seek Support Now'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='epds_results')
    score = models.PositiveSmallIntegerField()
    tier = models.CharField(max_length=20, choices=TIER_CHOICES)
    responses = models.JSONField(default=dict, help_text="Stores {question_id: answer_option_id} mapping")
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.user.email} — Score {self.score} ({self.get_tier_display()}) — {self.completed_at.date()}"

    @classmethod
    def calculate_tier(cls, score):
        if score <= 8:
            return cls.TIER_DOING_WELL
        elif score <= 12:
            return cls.TIER_NEEDS_ATTENTION
        else:
            return cls.TIER_SEEK_SUPPORT
