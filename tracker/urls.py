"""Feelio — Tracker URLs"""
from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.tracker_overview, name='overview'),
    path('checkin/', views.checkin_view, name='checkin'),
    path('journal/', views.journal_list, name='journal'),
    path('journal/new/', views.journal_new, name='journal_new'),
    path('journal/<int:pk>/edit/', views.journal_edit, name='journal_edit'),
    path('journal/<int:pk>/delete/', views.journal_delete, name='journal_delete'),
]
