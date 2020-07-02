from typing import List

from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from athletes.models import Athlete
from scores.models import Score
from wodmovements.models import Component
from wods.forms import WorkoutForm, AddScoreForm
from wods.models import Workout


class HttpResponseNotAllowedException(HttpResponseNotAllowed, Exception):

    def __init__(self, *args, **kwargs):
        super().__init__("Update/Delete only allowed if no data from other users is logged", *args, **kwargs)


class IndexView(generic.ListView):
    context_object_name = 'workout_list'

    def get_queryset(self):
        return Workout.objects.order_by('-date')[:25]


class DetailView(generic.DetailView):
    model = Workout

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scores'] = Score.objects.filter(workout_id=kwargs['object'].id).order_by('-logging_date')[:25]
        return context


class CreateView(LoginRequiredMixin, generic.CreateView):
    model = Workout
    form_class = WorkoutForm

    def form_valid(self, form):
        workout = form.save(commit=False)
        workout.set_metadata()
        workout.creator = Athlete.objects.get(user__username=get_user(self.request).username)
        workout.save()
        return super().form_valid(form)


def create_workout(request):
    ComponentsFormSet = modelformset_factory(Component, fields=('reps', 'movement'))
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '10',
        'form-0-reps': 1,
    }

    if request.method == 'POST':
        components_form_set = ComponentsFormSet(request.POST)
        workout_form = WorkoutForm(request.POST)
        if components_form_set.is_valid() and workout_form.is_valid():
            cleaned_components_data = components_form_set.cleaned_data
            component_list: List[Component] = []
            for components_datum in cleaned_components_data:
                reps_ = components_datum['reps']
                movement_ = components_datum['movement']
                component = Component.objects.get_or_create(reps=reps_, movement=movement_)
                component_list.append(component)

            cleaned_workout_data = workout_form.cleaned_data
            name_ = cleaned_workout_data['name']
            workout_style_ = cleaned_workout_data['workout_style']
            description_ = cleaned_workout_data['description']
            workout_duration_ = cleaned_workout_data['workout_duration']
            rounds_ = cleaned_workout_data['rounds']
            rep_schema_ = cleaned_workout_data['rep_schema']

            Workout.objects.create(name=name_,
                                   workout_style=workout_style_,
                                   description=description_,
                                   workout_duration=workout_duration_,
                                   rounds=rounds_,
                                   rep_schema=rep_schema_,
                                   creator_id=request.user.id
                                   )
        return HttpResponseRedirect(reverse('wods:index'))
    else:
        components_form_set = ComponentsFormSet(data=data)
        workout_form = WorkoutForm()
    return render(request, 'wods/workout_form.html', {
        'workout_form': workout_form,
        'component_formset': components_form_set,
    })


class UpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'wods/workout_update.html'

    def get_object(self, queryset=None):
        obj = super(UpdateView, self).get_object()
        if not obj.creator.id == get_user(self.request).athlete.id:
            raise HttpResponseForbidden

        if Score.objects.filter(workout_id=obj.id).exclude(athlete_id=obj.creator.id).exists():
            if self.request.method == 'GET':
                return None
            else:
                raise HttpResponseNotAllowedException

        return obj


class DeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Workout
    success_url = reverse_lazy('wods:index')

    def get_object(self, queryset=None):
        obj = super(DeleteView, self).get_object()
        if not obj.creator.id == get_user(self.request).athlete.id:
            raise HttpResponseForbidden

        if Score.objects.filter(workout_id=obj.id).exclude(athlete_id=obj.creator.id).exists():
            if self.request.method == 'GET':
                return None
            else:
                raise HttpResponseNotAllowedException

        return obj


class AddScoreView(LoginRequiredMixin, generic.UpdateView):
    model = Workout
    context_object_name = 'workout'
    form_class = AddScoreForm
    template_name = 'wods/add_score.html'

    def form_valid(self, form):
        workout = form.save(commit=False)
        score_ = form.cleaned_data['score']
        date_ = form.cleaned_data['execution_date']
        user = get_user(self.request)
        Score.objects.create(score=score_, execution_date=date_, workout=workout, athlete=user.athlete).save()
        return super().form_valid(form)
