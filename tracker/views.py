"""Feelio — Tracker Views"""
import json
import random
from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Avg
from .models import MoodEntry, JournalEntry, SymptomTag, JOURNAL_PROMPTS
from .forms import MoodCheckInForm, JournalEntryForm


@login_required
def tracker_overview(request):
    """Mood history calendar and chart data."""
    entries = MoodEntry.objects.filter(user=request.user).order_by('-date')[:90]

    # Build chart data for last 30 days
    today = timezone.localdate()
    chart_labels = []
    chart_data = []
    for i in range(29, -1, -1):
        d = today - timedelta(days=i)
        chart_labels.append(d.strftime('%b %d'))
        entry = next((e for e in entries if e.date == d), None)
        chart_data.append(entry.mood_score if entry else None)

    # Calendar data: last 90 days
    calendar_data = {}
    for entry in entries:
        calendar_data[entry.date.isoformat()] = {
            'score': entry.mood_score,
            'emoji': entry.mood_emoji,
            'label': entry.mood_label,
        }

    checked_in_today = MoodEntry.objects.filter(user=request.user, date=today).exists()

    return render(request, 'tracker/overview.html', {
        'entries': entries[:30],
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'calendar_data': json.dumps(calendar_data),
        'checked_in_today': checked_in_today,
        'today': today,
    })


@login_required
def checkin_view(request):
    """Daily mood check-in — one per day."""
    today = timezone.localdate()
    existing = MoodEntry.objects.filter(user=request.user, date=today).first()
    if existing:
        messages.info(request, "You've already checked in today! 🌸 Come back tomorrow.")
        return redirect('tracker:overview')

    if request.method == 'POST':
        form = MoodCheckInForm(request.POST, user=request.user)
        if form.is_valid():
            entry = form.save()
            messages.success(request, "Check-in saved! Your feelings matter. 💗")
            return redirect('dashboard:home')
    else:
        form = MoodCheckInForm(user=request.user)

    return render(request, 'tracker/checkin.html', {'form': form, 'today': today})


@login_required
def journal_list(request):
    """List all journal entries."""
    q = request.GET.get('q', '')
    entries = JournalEntry.objects.filter(user=request.user)
    if q:
        entries = entries.filter(content__icontains=q) | entries.filter(title__icontains=q)
    return render(request, 'tracker/journal_list.html', {'entries': entries, 'q': q})


@login_required
def journal_new(request):
    """Create a new journal entry."""
    prompt = random.choice(JOURNAL_PROMPTS)
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, "Journal entry saved. 🌙")
            return redirect('tracker:journal')
    else:
        form = JournalEntryForm(initial={'prompt_used': prompt})
    return render(request, 'tracker/journal_form.html', {'form': form, 'prompt': prompt, 'action': 'New'})


@login_required
def journal_edit(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Entry updated.")
            return redirect('tracker:journal')
    else:
        form = JournalEntryForm(instance=entry)
    return render(request, 'tracker/journal_form.html', {'form': form, 'action': 'Edit'})


@login_required
def journal_delete(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, "Entry deleted.")
        return redirect('tracker:journal')
    return render(request, 'tracker/journal_confirm_delete.html', {'entry': entry})
