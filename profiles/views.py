from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from athletes.models import Athlete
from profiles.forms import CustomUserCreationForm
from scores.models import Score
from wods.models import Workout


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


class ProfileView(generic.DetailView):
    template_name = 'profiles/profile.html'

    def get_object(self, queryset=None):
        athlete = Athlete.objects.get(user__username=self.request.user.username)
        return athlete

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_athlete_id = kwargs['object'].id
        context['scores'] = Score.objects.filter(athlete_id=view_athlete_id).order_by('-logging_date')[:25]
        context['workouts'] = Workout.objects.filter(creator_id=view_athlete_id).order_by('-date')[:25]
        return context
