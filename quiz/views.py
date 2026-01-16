from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db.models import Prefetch
from django.urls import reverse
from .models import Course, Session, Question, Choice, Attempt, Answer
from .forms import AnswerForm


def _get_or_create_attempt(request, session: Session):
    if not request.session.session_key:
        request.session.create()
    user = request.user if request.user.is_authenticated else None
    attempt = Attempt.objects.filter(
        session=session,
        user=user if user else None,
        session_key="" if user else request.session.session_key,
        finished_at__isnull=True,
    ).first()
    if not attempt:
        attempt = Attempt.objects.create(
            session=session,
            user=user if user else None,
            session_key="" if user else request.session.session_key,
            current_index=1,
        )
    return attempt


def course_list(request):
    courses = Course.objects.prefetch_related(
        Prefetch("sessions", queryset=Session.objects.filter(is_published=True))
    )
    return render(request, "quiz/course_list.html", {"courses": courses})


def session_detail(request, course_slug, session_slug):
    session = get_object_or_404(Session, course__slug=course_slug, slug=session_slug, is_published=True)
    return render(request, "quiz/session_detail.html", {"session": session})


def start_attempt(request, course_slug, session_slug):
    session = get_object_or_404(Session, course__slug=course_slug, slug=session_slug, is_published=True)
    attempt = _get_or_create_attempt(request, session)
    return redirect("quiz:run_question", course_slug=course_slug, session_slug=session_slug, index=attempt.current_index)


def run_question(request, course_slug, session_slug, index: int):
    session = get_object_or_404(Session, course__slug=course_slug, slug=session_slug, is_published=True)
    questions = list(session.questions.filter(is_active=True).prefetch_related("choices"))
    total = len(questions)
    if total == 0:
        return redirect("quiz:session_detail", course_slug=course_slug, session_slug=session_slug)
    # sınır kontrolü
    if index < 1: index = 1
    if index > total: index = total

    attempt = _get_or_create_attempt(request, session)
    attempt.current_index = index
    attempt.save(update_fields=["current_index"])

    q = questions[index - 1]
    form = AnswerForm()
    form.fields["choice_id"].queryset = q.choices.all()

    # Daha önce cevaplanmış mı kontrol et
    given = attempt.answers.filter(question=q).first()
    is_answered = given is not None
    
    feedback = None
    selected_id = None
    correct_choice = q.choices.filter(is_correct=True).first()
    just_answered = False
    
    # POST işlemi - şık seçildiğinde kaydet (sadece daha önce cevaplanmamışsa)
    if request.method == "POST" and not is_answered:
        form = AnswerForm(request.POST)
        form.fields["choice_id"].queryset = q.choices.all()
        if form.is_valid():
            choice = form.cleaned_data["choice_id"]
            # Yeni cevap oluştur
            ans = Answer.objects.create(
                attempt=attempt,
                question=q,
                choice=choice,
                is_correct=choice.is_correct
            )
            feedback = "correct" if ans.is_correct else "wrong"
            selected_id = choice.id
            form.initial = {"choice_id": selected_id}
            is_answered = True
            given = ans
            just_answered = True
    elif is_answered:
        # GET işlemi veya zaten cevaplanmış - daha önce cevaplanmışsa göster
        feedback = "correct" if given.is_correct else "wrong"
        selected_id = given.choice_id
        form.initial = {"choice_id": selected_id}

    # Sınav gezintisi için kutuların durumları
    states = []  # [(i, state)]
    for i, qq in enumerate(questions, start=1):
        a = attempt.answers.filter(question=qq).first()
        if not a:
            state = "blank"
        else:
            state = "ok" if a.is_correct else "fail"
        if i == index:
            state = f"current {state}"
        states.append((i, state))

    if index < total:
        next_url = reverse("quiz:run_question", kwargs={
            "course_slug": course_slug,
            "session_slug": session_slug,
            "index": index + 1,
        })
    else:
        next_url = reverse("quiz:finish_attempt", kwargs={
            "course_slug": course_slug,
            "session_slug": session_slug,
        })

    return render(request, "quiz/question_run.html", {
        "session": session,
        "q": q,
        "form": form,
        "index": index,
        "total": total,
        "feedback": feedback,
        "selected_id": selected_id,
        "states": states,
        "is_answered": is_answered,
        "correct_choice": correct_choice,
        "given_answer": given,
        "just_answered": just_answered,
        "next_url": next_url,
        "auto_advance": session.course.slug == 'fiba',  # FIBA için otomatik geçme
    })


def finish_attempt(request, course_slug, session_slug):
    session = get_object_or_404(Session, course__slug=course_slug, slug=session_slug, is_published=True)
    attempt = _get_or_create_attempt(request, session)
    if not attempt.finished_at:
        attempt.finished_at = timezone.now()
        attempt.save(update_fields=["finished_at"])

    # Tüm soruları ve cevapları getir
    all_answers = (
        attempt.answers
        .select_related("question", "choice")
        .prefetch_related("question__choices")
        .order_by("question__order")
    )
    
    # Yanlış cevapları ayrı liste
    wrong_items = attempt.answers.filter(is_correct=False).select_related("question", "choice")
    
    wrongs_data = []
    for a in wrong_items:
        correct_choice = a.question.choices.filter(is_correct=True).first()
        wrongs_data.append({
            "question": a.question,
            "your": a.choice,
            "correct": correct_choice
        })
    
    # Tüm sorular ve cevaplar
    all_questions_data = []
    for a in all_answers:
        correct_choice = a.question.choices.filter(is_correct=True).first()
        all_questions_data.append({
            "question": a.question,
            "your": a.choice,
            "correct": correct_choice,
            "is_correct": a.is_correct
        })

    return render(request, "quiz/result_summary.html", {
        "session": session,
        "attempt": attempt,
        "total": attempt.total_questions(),
        "correct": attempt.correct_count(),
        "wrong": attempt.wrong_count(),
        "wrongs": wrongs_data,
        "all_questions": all_questions_data,
    })
