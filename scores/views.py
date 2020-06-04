from django.views import generic

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
