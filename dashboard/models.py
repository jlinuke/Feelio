"""Feelio — Dashboard App Models"""
from django.db import models
from django.conf import settings


class DailyAffirmation(models.Model):
    text_en = models.TextField()
    text_si = models.TextField(blank=True)
    text_ta = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.text_en[:80]


class CheckInStreak(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='streak')
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_checkin_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} — {self.current_streak} days"

    def update(self, checkin_date):
        from datetime import timedelta
        if self.last_checkin_date:
            if checkin_date == self.last_checkin_date + timedelta(days=1):
                self.current_streak += 1
            elif checkin_date > self.last_checkin_date:
                self.current_streak = 1
            # same day — no change
        else:
            self.current_streak = 1
        self.longest_streak = max(self.longest_streak, self.current_streak)
        self.last_checkin_date = checkin_date
        self.save()
