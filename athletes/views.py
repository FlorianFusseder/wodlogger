from django.views import generic

from athletes.models import Athlete


class IndexView(generic.ListView):
    context_object_name = 'athlete_list'

    def get_queryset(self):
        return Athlete.objects.order_by('last_name')[:25]


class DetailView(generic.DetailView):
    model = Athlete


class UpdateView(generic.UpdateView):
    model = Athlete
    fields = ['first_name', 'last_name']

    def get_object(self, queryset=None):
        athlete = Athlete.objects.get(user__username=self.request.user.username)
        return athlete
