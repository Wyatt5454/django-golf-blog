from django.urls import path

from . import views

app_name = "rounds"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]