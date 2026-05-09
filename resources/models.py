"""Feelio — Resources App Models"""
from django.db import models
from django.utils.text import slugify


class Helpline(models.Model):
    name = models.CharField(max_length=120)
    number = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    available_hours = models.CharField(max_length=60, default='24/7')
    languages = models.CharField(max_length=80, default='Sinhala, Tamil, English')
    is_featured = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['-is_featured', 'order']

    def __str__(self):
        return f"{self.name} — {self.number}"


class Article(models.Model):
    CATEGORY_CHOICES = [
        ('myth_busting', 'Myth Busting'),
        ('understanding_ppd', 'Understanding PPD'),
        ('for_family', 'For Partners & Family'),
        ('treatment', 'Treatment Options'),
        ('general', 'General'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='general')
    summary = models.TextField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class PHMContact(models.Model):
    """Public Health Midwife contact entry."""
    name = models.CharField(max_length=120, blank=True)
    province = models.CharField(max_length=60)
    district = models.CharField(max_length=60)
    moh_office = models.CharField(max_length=120, blank=True, help_text='MOH office name')
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['province', 'district']
        verbose_name = 'PHM Contact'
        verbose_name_plural = 'PHM Contacts'

    def __str__(self):
        return f"{self.district} — {self.moh_office}"
