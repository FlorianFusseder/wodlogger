from django.contrib.auth import get_user
from django.views import generic

from athletes.models import Athlete
from wods.forms import WorkoutForm
from wods.models import Workout


class IndexView(generic.ListView):
    context_object_name = 'workout_list'

    def get_queryset(self):
        return Workout.objects.order_by('-date')[:25]


class DetailView(generic.DetailView):
    model = Workout


class CreateView(generic.edit.CreateView):
    model = Workout
    form_class = WorkoutForm

    def form_valid(self, form):
        workout = form.save(commit=False)
        workout.creator = Athlete.objects.get(user__username=get_user(self.request).username)
        workout.save()
        return super().form_valid(form)
