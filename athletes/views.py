from django.views import generic

from athletes.models import Athlete


class IndexView(generic.ListView):
    context_object_name = 'athlete_list'

    def get_queryset(self):
        return Athlete.objects.order_by('last_name')[:25]


class DetailView(generic.DetailView):
    model = Athlete


class CreateView(generic.edit.CreateView):
    model = Athlete
    fields = ['first_name', 'last_name']


