"""Feelio — Resources Views"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Helpline, Article, PHMContact


def resources_home(request):
    featured_helplines = Helpline.objects.filter(is_featured=True)
    recent_articles = Article.objects.filter(is_published=True)[:6]
    return render(request, 'resources/home.html', {
        'featured_helplines': featured_helplines,
        'recent_articles': recent_articles,
    })


def helplines_view(request):
    helplines = Helpline.objects.all()
    return render(request, 'resources/helplines.html', {'helplines': helplines})


def articles_list(request):
    category = request.GET.get('category', '')
    articles = Article.objects.filter(is_published=True)
    if category:
        articles = articles.filter(category=category)
    categories = Article.CATEGORY_CHOICES
    return render(request, 'resources/articles_list.html', {
        'articles': articles,
        'categories': categories,
        'selected_category': category,
    })


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    related = Article.objects.filter(category=article.category, is_published=True).exclude(pk=article.pk)[:3]
    return render(request, 'resources/article_detail.html', {'article': article, 'related': related})


def phm_locator(request):
    province = request.GET.get('province', '')
    contacts = PHMContact.objects.filter(is_active=True)
    if province:
        contacts = contacts.filter(province__icontains=province)
    provinces = PHMContact.objects.filter(is_active=True).values_list('province', flat=True).distinct()
    return render(request, 'resources/phm_locator.html', {
        'contacts': contacts,
        'provinces': provinces,
        'selected_province': province,
    })
