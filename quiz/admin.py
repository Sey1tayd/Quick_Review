from django.contrib import admin
from .models import Course, Session, Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("session", "order", "text", "is_active")
    list_filter = ("session", "is_active")
    ordering = ("session", "order")


admin.site.register(Course)
admin.site.register(Session)
