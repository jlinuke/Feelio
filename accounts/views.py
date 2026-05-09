"""Feelio — Accounts Views"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import RegisterForm, LoginForm, ProfileSetupForm, UserSettingsForm
from .models import UserProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, _("Welcome to Feelio! Let's set up your profile."))
            return redirect('accounts:profile_setup')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, _(f"Welcome back, {user.community_name}!"))
            return redirect(request.GET.get('next', 'dashboard:home'))
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, _("You've been logged out. Take care! 💗"))
    return redirect('/')


@login_required
def profile_setup_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileSetupForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _("Profile saved! Your Feelio journey begins now. 🌸"))
            return redirect('dashboard:home')
    else:
        form = ProfileSetupForm(instance=profile)
    return render(request, 'accounts/profile_setup.html', {'form': form})


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    user_form = UserSettingsForm(instance=request.user)
    profile_form = ProfileSetupForm(instance=profile)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'user_settings':
            user_form = UserSettingsForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, _("Settings updated!"))
                return redirect('accounts:profile')
        elif action == 'profile_settings':
            profile_form = ProfileSetupForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, _("Profile updated!"))
                return redirect('accounts:profile')
        elif action == 'delete_account':
            request.user.delete()
            messages.info(request, _("Your account and all data have been permanently deleted."))
            return redirect('/')

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
    })
