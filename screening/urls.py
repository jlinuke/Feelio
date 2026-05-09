"""Feelio — Screening URLs"""
from django.urls import path
from . import views

app_name = 'screening'

urlpatterns = [
    path('', views.screening_start, name='start'),
    path('take/', views.screening_take, name='take'),
    path('result/<int:pk>/', views.screening_result, name='result'),
    path('history/', views.screening_history, name='history'),
]
