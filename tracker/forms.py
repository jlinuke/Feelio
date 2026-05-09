"""Feelio — Tracker Forms"""
from django import forms
from django.utils import timezone
from .models import MoodEntry, JournalEntry, SymptomTag


class MoodCheckInForm(forms.ModelForm):
    mood_score = forms.ChoiceField(
        choices=MoodEntry.MOOD_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'mood-radio'}),
        label='How are you feeling today?'
    )
    symptoms = forms.ModelMultipleChoiceField(
        queryset=SymptomTag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'symptom-checkbox'}),
        required=False,
        label='Any of these today?'
    )

    class Meta:
        model = MoodEntry
        fields = ('mood_score', 'one_word_feeling', 'symptoms',
                  'breastfeeding_difficulty', 'physical_pain', 'medication_reminder', 'notes')
        widgets = {
            'one_word_feeling': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. tired, hopeful, overwhelmed…',
                'maxlength': '40'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Anything else you want to note? (optional)'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        entry = super().save(commit=False)
        entry.user = self.user
        entry.date = timezone.localdate()
        if commit:
            entry.save()
            self.save_m2m()
        return entry


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ('title', 'content', 'prompt_used', 'is_pinned')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Entry title (optional)'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control journal-editor',
                'rows': 12,
                'placeholder': 'Pour your heart out here. This is your safe space. 💗'
            }),
            'prompt_used': forms.HiddenInput(),
            'is_pinned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
