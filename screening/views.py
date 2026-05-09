"""Feelio — Screening Views: EPDS flow"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import EPDSQuestion, EPDSAnswerOption, EPDSResult


@login_required
def screening_start(request):
    """EPDS introduction page."""
    last_result = EPDSResult.objects.filter(user=request.user).first()
    return render(request, 'screening/start.html', {'last_result': last_result})


@login_required
def screening_take(request):
    """Handle EPDS question flow. Stores answers in session."""
    questions = list(EPDSQuestion.objects.prefetch_related('options').all())
    if not questions:
        messages.warning(request, "The screening questions haven't been set up yet. Please check back soon.")
        return redirect('screening:start')

    if request.method == 'POST':
        answers = {}
        total_score = 0
        valid = True

        for q in questions:
            ans_id = request.POST.get(f'q_{q.id}')
            if not ans_id:
                valid = False
                break
            try:
                option = EPDSAnswerOption.objects.get(pk=ans_id, question=q)
                raw_score = option.score_value
                # Reverse scoring for applicable questions
                score = (3 - raw_score) if q.is_reverse_scored else raw_score
                answers[str(q.id)] = ans_id
                total_score += score
            except EPDSAnswerOption.DoesNotExist:
                valid = False
                break

        if not valid:
            messages.error(request, "Please answer all questions before submitting.")
            return render(request, 'screening/take.html', {'questions': questions})

        tier = EPDSResult.calculate_tier(total_score)
        result = EPDSResult.objects.create(
            user=request.user,
            score=total_score,
            tier=tier,
            responses=answers,
        )
        return redirect('screening:result', pk=result.pk)

    return render(request, 'screening/take.html', {'questions': questions})


@login_required
def screening_result(request, pk):
    """Display EPDS result with tier-based guidance."""
    result = get_object_or_404(EPDSResult, pk=pk, user=request.user)
    return render(request, 'screening/result.html', {'result': result})


@login_required
def screening_history(request):
    """Past EPDS scores."""
    results = EPDSResult.objects.filter(user=request.user)
    return render(request, 'screening/history.html', {'results': results})
