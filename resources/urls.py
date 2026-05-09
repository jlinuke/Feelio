"""Feelio — Resources URLs"""
from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.resources_home, name='home'),
    path('helplines/', views.helplines_view, name='helplines'),
    path('articles/', views.articles_list, name='articles'),
    path('articles/<slug:slug>/', views.article_detail, name='article_detail'),
    path('phm/', views.phm_locator, name='phm'),
]
