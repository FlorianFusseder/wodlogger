from django.contrib.auth import get_user
from django.views import generic

from athletes.models import Athlete
from scores.forms import ScoreForm
from scores.models import Score


class IndexView(generic.ListView):
    context_object_name = 'score_list'

    def get_queryset(self):
        return Score.objects.order_by('-date')[:25]


class DetailView(generic.DetailView):
    model = Score


class CreateView(generic.edit.CreateView):
    model = Score
    form_class = ScoreForm

    def form_valid(self, form):
        score = form.save(commit=False)
        score.athlete = Athlete.objects.get(user__username=get_user(self.request).username)
        score.save()
        return super().form_valid(form)
