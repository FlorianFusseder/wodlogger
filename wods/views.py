import logging

from django.forms import DateTimeInput
from django.views import generic

from wods.forms import WorkoutForm
from wods.models import Workout

logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    context_object_name = 'workout_list'

    def get_queryset(self):
        return Workout.objects.order_by('-pub_date')[:25]


class DetailView(generic.DetailView):
    model = Workout


class CreateView(generic.edit.CreateView):
    model = Workout
    form_class = WorkoutForm
