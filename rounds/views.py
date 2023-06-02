from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Round

# Create your views here.
class IndexView(generic.ListView):
    template_name = "rounds/index.html"
    context_object_name = "round_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Round.objects.filter(play_date__lte=timezone.now()).filter(holescore__gt=0).distinct().order_by("-play_date")[
        :5 
        ]