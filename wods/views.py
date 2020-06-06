from django.contrib.auth import get_user
from django.views import generic

from athletes.models import Athlete
from scores.models import Score
from wods.forms import WorkoutForm, AddScoreForm
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


class AddScoreView(generic.UpdateView):
    model = Workout
    context_object_name = 'workout'
    form_class = AddScoreForm
    template_name = 'wods/add_score.html'

    def form_valid(self, form):
        workout = form.save(commit=False)
        score_ = form.cleaned_data['score']
        date_ = form.cleaned_data['date']
        user = get_user(self.request)
        Score.objects.create(score=score_, date=date_, workout=workout, athlete=user.athlete).save()
        return super().form_valid(form)

