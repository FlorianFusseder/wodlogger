from django.contrib.auth import get_user
from django.views import generic

from athletes.models import Athlete
from scores.models import Score
from wods.models import Workout


class IndexView(generic.ListView):
    context_object_name = 'athlete_list'

    def get_queryset(self):
        return Athlete.objects.order_by('last_name')[:25]


class DetailView(generic.DetailView):
    model = Athlete

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user(self.request)
        current_athlete_id = Athlete.objects.get(user_id=user.id).id
        view_athlete_id = kwargs['object'].id
        context['scores'] = Score.objects.filter(athlete_id=current_athlete_id) \
                                .order_by('-logging_date')[:25]
        context['workouts'] = Workout.objects.filter(creator_id=view_athlete_id) \
                                  .order_by('-date')[:25]
        return context


class UpdateView(generic.UpdateView):
    model = Athlete
    fields = ['first_name', 'last_name']

    def get_object(self, queryset=None):
        athlete = Athlete.objects.get(user__username=self.request.user.username)
        return athlete
