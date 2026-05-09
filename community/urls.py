"""Feelio — Community URLs"""
from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.forum_home, name='forum'),
    path('category/<slug:slug>/', views.forum_category, name='category'),
    path('thread/<int:pk>/', views.thread_detail, name='thread'),
    path('thread/new/', views.new_thread, name='new_thread'),
    path('thread/new/<slug:category_slug>/', views.new_thread, name='new_thread_category'),
    path('post/<int:post_pk>/react/', views.toggle_reaction, name='react'),
    path('post/<int:post_pk>/flag/', views.flag_post, name='flag'),
    path('msgs/', views.msg_directory, name='msgs'),
]
