from django.urls import path
from . import views

app_name = "quiz"

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("<slug:course_slug>/<slug:session_slug>/", views.session_detail, name="session_detail"),
    path("<slug:course_slug>/<slug:session_slug>/start/", views.start_attempt, name="start_attempt"),
    path("<slug:course_slug>/<slug:session_slug>/q/<int:index>/", views.run_question, name="run_question"),
    path("<slug:course_slug>/<slug:session_slug>/finish/", views.finish_attempt, name="finish_attempt"),
]


