"""Feelio — Community Forms"""
from django import forms
from .models import ForumThread, Post, ForumCategory


class ThreadForm(forms.ModelForm):
    class Meta:
        model = ForumThread
        fields = ('category', 'title', 'content')
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'What do you want to talk about?'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Share your thoughts, questions, or story. This is a safe space. 💗'}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your reply here. Be kind — we are all in this together. 💗'
            }),
        }
        labels = {'content': ''}
