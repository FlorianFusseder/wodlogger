from django.contrib.auth import get_user
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views import generic

from scores.forms import ScoreForm
from scores.models import Score


class IndexView(generic.ListView):
    context_object_name = 'score_list'

    def get_queryset(self):
        return Score.objects.order_by('-logging_date')[:25]


class DetailView(generic.DetailView):
    model = Score


class UpdateView(generic.UpdateView):
    model = Score
    form_class = ScoreForm


class DeleteView(generic.DeleteView):
    model = Score
    success_url = reverse_lazy('score:index')

    def get_object(self, queryset=None):
        obj = super(DeleteView, self).get_object()
        if not obj.athlete.id == get_user(self.request).athlete.id:
            raise HttpResponseForbidden
        return obj
