from django.urls import path

from . import views

app_name = "rounds"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("course/<slug:slug>/", views.CourseView.as_view(), name="course"),
    path("api/rounds", views.APIView.rounds_api, name="rounds api"),
]