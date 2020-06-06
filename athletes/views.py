from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from athletes.forms import CustomUserCreationForm
from athletes.models import Athlete


class IndexView(generic.ListView):
    context_object_name = 'athlete_list'

    def get_queryset(self):
        return Athlete.objects.order_by('last_name')[:25]


class DetailView(generic.DetailView):
    model = Athlete


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('athletes:profile')
    template_name = 'athletes/athlete_signup.html'

    def form_valid(self, form):
        user = form.save()
        user.athlete = Athlete.objects.create(first_name=form.cleaned_data['first_name'], user=user)
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], )
        login(self.request, user)
        return HttpResponseRedirect(reverse('athletes:profile'))
