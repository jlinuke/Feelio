"""Feelio — Accounts Forms"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': _('your@email.com'), 'class': 'form-control form-control-lg'})
    )
    first_name = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={'placeholder': _('Your first name'), 'class': 'form-control form-control-lg'})
    )
    display_alias = forms.CharField(
        max_length=60, required=False,
        widget=forms.TextInput(attrs={'placeholder': _('e.g. StrongMama (optional)'), 'class': 'form-control form-control-lg'}),
        help_text=_('This alias will be shown in the community instead of your real name.')
    )
    is_anonymous_mode = forms.BooleanField(required=False, label=_('Use anonymous alias in community'))

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'display_alias', 'is_anonymous_mode', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault('class', 'form-control form-control-lg')
        self.fields['password1'].widget.attrs['placeholder'] = _('Password (min 8 chars)')
        self.fields['password2'].widget.attrs['placeholder'] = _('Confirm password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Use email as username
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'placeholder': _('your@email.com'), 'class': 'form-control form-control-lg', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'form-control form-control-lg'})
    )


class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('baby_due_date', 'baby_birth_date', 'is_first_time_mother', 'province', 'district',
                  'share_data_for_research', 'daily_reminder_time', 'weekly_screening_reminder')
        widgets = {
            'baby_due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-lg'}),
            'baby_birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-lg'}),
            'province': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'district': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'e.g. Colombo'}),
            'daily_reminder_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control form-control-lg'}),
        }


class UserSettingsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    display_alias = forms.CharField(max_length=60, required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    language_preference = forms.ChoiceField(
        choices=[('en', 'English'), ('si', 'සිංහල'), ('ta', 'தமிழ்')],
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    )
    is_anonymous_mode = forms.BooleanField(required=False, label=_('Anonymous mode in community'))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'display_alias', 'language_preference', 'is_anonymous_mode')
