from django.conf import settings
from django.db import models


class Course(models.Model):  # Ders
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Session(models.Model):  # Oturum
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sessions")
    title = models.CharField(max_length=150)
    slug = models.SlugField()
    is_published = models.BooleanField(default=True)

    class Meta:
        unique_together = ("course", "slug")
        ordering = ["id"]

    def __str__(self):
        return f"{self.course} / {self.title}"

    def question_count(self):
        return self.questions.filter(is_active=True).count()


class Question(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    explanation = models.TextField(blank=True, help_text="Açıklama ve yorum (cevap verildikten sonra gösterilir)")

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"Q{self.order}: {self.text[:40]}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.text


# Sınav denemesi: login zorunlu değil; anonim kullanıcılar session_key ile tutulur
class Attempt(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="attempts")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40, blank=True)  # anonim kullanıcılar için
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    current_index = models.PositiveIntegerField(default=1)  # 1-based index

    def total_questions(self):
        return self.session.question_count()

    def correct_count(self):
        return self.answers.filter(is_correct=True).count()

    def wrong_count(self):
        return self.answers.filter(is_correct=False).count()


class Answer(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("attempt", "question")
