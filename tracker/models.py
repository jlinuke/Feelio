"""Feelio — Tracker App Models: MoodEntry, SymptomTag, JournalEntry"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class SymptomTag(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class MoodEntry(models.Model):
    MOOD_CHOICES = [
        (5, '😊 Joyful'),
        (4, '🙂 Okay'),
        (3, '😢 Sad'),
        (2, '😰 Anxious'),
        (1, '😶 Numb'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mood_entries')
    date = models.DateField()
    mood_score = models.PositiveSmallIntegerField(choices=MOOD_CHOICES)
    one_word_feeling = models.CharField(max_length=40, blank=True)
    symptoms = models.ManyToManyField(SymptomTag, blank=True)

    # Physical notes
    breastfeeding_difficulty = models.BooleanField(default=False)
    physical_pain = models.BooleanField(default=False)
    medication_reminder = models.BooleanField(default=False)

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.email} — {self.date} — {self.get_mood_score_display()}"

    @property
    def mood_emoji(self):
        return self.get_mood_score_display().split(' ')[0]

    @property
    def mood_label(self):
        return ' '.join(self.get_mood_score_display().split(' ')[1:])


class JournalEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='journal_entries')
    title = models.CharField(max_length=120, blank=True)
    content = models.TextField()
    prompt_used = models.CharField(max_length=255, blank=True)
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} — {self.created_at.strftime('%Y-%m-%d %H:%M')}"


# Sample journal prompts (loaded as fixture or from DB)
JOURNAL_PROMPTS = [
    "What is one thing your body did for you today?",
    "Describe a moment today when you felt most like yourself.",
    "What is one small thing you are proud of as a mother?",
    "What emotions came up for you today, and where did you feel them in your body?",
    "Write a kind message to yourself as if you were writing to a dear friend.",
    "What do you need most right now that you're not getting?",
    "Describe your baby's face. What does it make you feel?",
    "What support would make the biggest difference for you this week?",
    "List three things, however small, that went well today.",
    "What would you tell a new mother who was feeling exactly like you do right now?",
]
