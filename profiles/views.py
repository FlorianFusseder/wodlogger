from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from athletes.models import Athlete
from profiles.forms import CustomUserCreationForm


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('profile:profile')
    template_name = 'profiles/signup.html'

    def form_valid(self, form):
        user = form.save()
        user.athlete = Athlete.objects.create(first_name=form.cleaned_data['first_name'],
                                              last_name=form.cleaned_data['last_name'],
                                              user=user)
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], )
        login(self.request, user)
        return HttpResponseRedirect(reverse('profiles:profile'))
