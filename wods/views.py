import logging

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.views import generic

from wods.models import Workout

logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    context_object_name = 'workout_list'

    def get_queryset(self):
        return Workout.objects.order_by('-pub_date')[:25]


class DetailView(generic.DetailView):
    model = Workout


class CreateView(generic.CreateView):
    model = Workout
