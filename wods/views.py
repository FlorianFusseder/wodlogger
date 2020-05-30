import logging

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader

from wods.models import Workout

logger = logging.getLogger(__name__)


def index(request):
    wods = Workout.objects.order_by('-pub_date')[:25]
    return render(request, "wods/index.html", {'latest_workouts_list': wods})


def detail(request, workout_id):
    logger.info(f"Get workout with id {workout_id}")
    workout = get_object_or_404(Workout, id=workout_id)
    return render(request, "wods/detail.html", {'workout': workout})


def create(request, workout_id):
    return HttpResponse(f"You're voting on workout {workout_id}.")
