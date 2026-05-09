"""Feelio — Community Views"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import ForumCategory, ForumThread, Post, Reaction, FlaggedPost, MSGLocation, CRISIS_KEYWORDS
from .forms import ThreadForm, PostForm


@login_required
def forum_home(request):
    categories = ForumCategory.objects.prefetch_related('threads').all()
    recent_threads = ForumThread.objects.select_related('author', 'category').order_by('-updated_at')[:10]
    return render(request, 'community/forum_home.html', {
        'categories': categories,
        'recent_threads': recent_threads,
    })


@login_required
def forum_category(request, slug):
    category = get_object_or_404(ForumCategory, slug=slug)
    threads = category.threads.select_related('author').order_by('-is_pinned', '-updated_at')
    paginator = Paginator(threads, 15)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'community/forum_category.html', {'category': category, 'page': page})


@login_required
def thread_detail(request, pk):
    thread = get_object_or_404(ForumThread, pk=pk)
    thread.view_count += 1
    thread.save(update_fields=['view_count'])

    posts = thread.posts.select_related('author').prefetch_related('reactions')
    post_form = PostForm()

    if request.method == 'POST' and not thread.is_closed:
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.thread = thread
            post.author = request.user

            # Crisis keyword detection
            content_lower = post.content.lower()
            crisis_detected = any(kw in content_lower for kw in CRISIS_KEYWORDS)
            post.save()

            if crisis_detected:
                # Flag for moderator and show crisis resources
                FlaggedPost.objects.get_or_create(post=post, flagged_by=request.user, defaults={'reason': 'AUTO: Crisis keyword detected'})
                messages.warning(request, "We noticed you might be going through a very hard time. Please reach out to the NIMH helpline: 📞 1926. You are not alone. 💗")
            else:
                messages.success(request, "Your reply has been posted.")
            return redirect('community:thread', pk=thread.pk)

    return render(request, 'community/thread_detail.html', {
        'thread': thread,
        'posts': posts,
        'post_form': post_form,
    })


@login_required
def new_thread(request, category_slug=None):
    category = get_object_or_404(ForumCategory, slug=category_slug) if category_slug else None
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            messages.success(request, "Your post is live! Other mothers can see and support you. 🌸")
            return redirect('community:thread', pk=thread.pk)
    else:
        form = ThreadForm(initial={'category': category})
    return render(request, 'community/thread_form.html', {'form': form, 'category': category})


@login_required
@require_POST
def toggle_reaction(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    reaction_type = request.POST.get('reaction_type')
    if reaction_type not in ['heart', 'hug', 'metoo']:
        return JsonResponse({'error': 'Invalid reaction'}, status=400)

    reaction, created = Reaction.objects.get_or_create(
        post=post, user=request.user, reaction_type=reaction_type
    )
    if not created:
        reaction.delete()
        active = False
    else:
        active = True

    counts = {
        'heart': post.reactions.filter(reaction_type='heart').count(),
        'hug': post.reactions.filter(reaction_type='hug').count(),
        'metoo': post.reactions.filter(reaction_type='metoo').count(),
    }
    return JsonResponse({'active': active, 'counts': counts})


@login_required
@require_POST
def flag_post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    reason = request.POST.get('reason', '')
    FlaggedPost.objects.get_or_create(post=post, flagged_by=request.user, defaults={'reason': reason})
    messages.info(request, "This post has been flagged for review. Thank you for keeping our community safe.")
    return redirect('community:thread', pk=post.thread.pk)


@login_required
def msg_directory(request):
    province = request.GET.get('province', '')
    locations = MSGLocation.objects.filter(is_active=True)
    if province:
        locations = locations.filter(province__icontains=province)
    provinces = MSGLocation.objects.filter(is_active=True).values_list('province', flat=True).distinct()
    return render(request, 'community/msg_directory.html', {
        'locations': locations,
        'provinces': provinces,
        'selected_province': province,
    })
