"""Feelio — Community App Models"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ForumCategory(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=40, default='fa-comments', help_text='Font Awesome icon class')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Forum Categories'

    def __str__(self):
        return self.name


class ForumThread(models.Model):
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, related_name='threads')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='threads')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_pinned = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-updated_at']

    def __str__(self):
        return self.title

    @property
    def author_display(self):
        return self.author.community_name if self.author else "Anonymous"

    @property
    def reply_count(self):
        return self.posts.count()


class Post(models.Model):
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_flagged = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Post by {self.author_display} in '{self.thread.title}'"

    @property
    def author_display(self):
        return self.author.community_name if self.author else "Anonymous"


class Reaction(models.Model):
    REACTION_CHOICES = [
        ('heart', '❤️ Heart'),
        ('hug', '🤗 Hug'),
        ('metoo', '🙋 Me too'),
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user', 'reaction_type')

    def __str__(self):
        return f"{self.user.community_name} reacted {self.reaction_type} to post {self.post.id}"


class FlaggedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='flags')
    flagged_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)
    is_reviewed = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reviewed_flags'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Flag on post {self.post.id} by {self.flagged_by.email}"


class MSGLocation(models.Model):
    """Mothers' Support Group directory entry."""
    name = models.CharField(max_length=200)
    province = models.CharField(max_length=60)
    district = models.CharField(max_length=60)
    address = models.TextField(blank=True)
    meeting_day = models.CharField(max_length=20, blank=True, help_text='e.g. Every Tuesday')
    meeting_time = models.CharField(max_length=20, blank=True, help_text='e.g. 9:00 AM')
    phm_contact_name = models.CharField(max_length=120, blank=True)
    phm_contact_phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['province', 'district', 'name']
        verbose_name = 'Mothers Support Group'
        verbose_name_plural = "Mothers' Support Groups"

    def __str__(self):
        return f"{self.name} — {self.district}"


# Crisis keywords for detection
CRISIS_KEYWORDS = [
    'want to disappear', "can't go on", 'end my life', 'kill myself',
    'not worth living', 'want to die', 'suicidal', 'hurt myself',
    'no reason to live', 'better off without me',
]
