"""Feelio — Dashboard Views"""
import random
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from tracker.models import MoodEntry
from community.models import ForumThread
from .models import DailyAffirmation, CheckInStreak

# Fallback affirmations if DB is empty
FALLBACK_AFFIRMATIONS = [
    "You are doing an incredible job, even on the hardest days. 💗",
    "Your love for your baby is clear in every breath you take.",
    "Rest is not weakness — it is wisdom.",
    "Asking for help is one of the bravest things a mother can do.",
    "You are not alone. There are hands reaching out to hold you.",
    "Every small step forward counts. You are moving forward.",
    "Your feelings are valid. All of them.",
    "You grew a human being. That is extraordinary.",
    "Today, be as gentle with yourself as you are with your baby.",
    "The fact that you care so much already makes you a wonderful mother.",
]


def landing_page(request):
    """Public landing page for unauthenticated users."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    return render(request, 'dashboard/landing.html')


@login_required
def dashboard_home(request):
    user = request.user
    today = timezone.localdate()

    # Today's check-in
    today_entry = MoodEntry.objects.filter(user=user, date=today).first()
    checked_in_today = today_entry is not None

    # Streak
    streak, _ = CheckInStreak.objects.get_or_create(user=user)

    # Crisis detection: 2+ days of "Numb" or "Anxious" (score 1 or 2)
    recent_moods = list(MoodEntry.objects.filter(
        user=user, date__gte=today - timedelta(days=2)
    ).values_list('mood_score', flat=True))
    show_crisis_banner = len(recent_moods) >= 2 and all(s <= 2 for s in recent_moods[:2])

    # Weekly mood chart data
    week_labels = []
    week_scores = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        week_labels.append(d.strftime('%a'))
        entry = MoodEntry.objects.filter(user=user, date=d).first()
        week_scores.append(entry.mood_score if entry else None)

    # Daily affirmation
    affirmations = list(DailyAffirmation.objects.filter(is_active=True))
    if affirmations:
        # Deterministic by day so it doesn't change on reload
        affirmation_text = affirmations[today.toordinal() % len(affirmations)].text_en
    else:
        affirmation_text = random.choice(FALLBACK_AFFIRMATIONS)

    # Community highlight
    community_highlight = ForumThread.objects.order_by('-updated_at').first()

    return render(request, 'dashboard/home.html', {
        'today': today,
        'today_entry': today_entry,
        'checked_in_today': checked_in_today,
        'streak': streak,
        'show_crisis_banner': show_crisis_banner,
        'week_labels': week_labels,
        'week_scores': week_scores,
        'affirmation': affirmation_text,
        'community_highlight': community_highlight,
    })
