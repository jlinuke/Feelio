"""
Feelio — Accounts App Models
CustomUser, UserProfile
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """Extended user with email-first auth and alias support."""
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=20, blank=True)
    display_alias = models.CharField(max_length=60, blank=True, help_text=_('Anonymous display name for community'))
    is_anonymous_mode = models.BooleanField(default=False, help_text=_('Hide real name in community'))
    language_preference = models.CharField(
        max_length=5,
        choices=[('en', 'English'), ('si', 'සිංහල'), ('ta', 'தமிழ்')],
        default='en'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def community_name(self):
        """Return alias if anonymous mode, else first name or email prefix."""
        if self.is_anonymous_mode and self.display_alias:
            return self.display_alias
        return self.first_name or self.email.split('@')[0]


class UserProfile(models.Model):
    """Extended profile linked 1-to-1 with CustomUser."""
    PROVINCE_CHOICES = [
        ('western', 'Western'), ('central', 'Central'), ('southern', 'Southern'),
        ('northern', 'Northern'), ('eastern', 'Eastern'), ('north_western', 'North Western'),
        ('north_central', 'North Central'), ('uva', 'Uva'), ('sabaragamuwa', 'Sabaragamuwa'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    baby_due_date = models.DateField(null=True, blank=True)
    baby_birth_date = models.DateField(null=True, blank=True)
    is_first_time_mother = models.BooleanField(default=True)
    province = models.CharField(max_length=30, choices=PROVINCE_CHOICES, blank=True)
    district = models.CharField(max_length=60, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    # Privacy toggles
    share_data_for_research = models.BooleanField(default=False)
    daily_reminder_time = models.TimeField(null=True, blank=True)
    weekly_screening_reminder = models.BooleanField(default=True)

    # Journal PIN
    journal_pin = models.CharField(max_length=128, blank=True, help_text=_('Hashed PIN for journal lock'))

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.email}"
