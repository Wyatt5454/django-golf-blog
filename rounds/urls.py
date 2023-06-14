from django.urls import path

from . import views
from . import api

app_name = "rounds"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("course/<slug:slug>/", views.CourseView.as_view(), name="course"),
    path("api/rounds", api.APIView.all_rounds, name="all rounds"),
    path("api/rounds/<int:round_id>/", api.APIView.round_by_pk, name="round by pk"),
]