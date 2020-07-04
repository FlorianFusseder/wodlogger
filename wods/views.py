from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views import generic

from athletes.models import Athlete
from scores.models import Score
from wodmovements.forms import ComponentForm
from wodmovements.models import Component, Movement
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
    ComponentsFormSet = modelformset_factory(Component, form=ComponentForm, min_num=1)
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '10',
        'form-0-reps': 1,
    }

    if request.is_ajax():
        query_term = request.GET.get('q')
        if query_term:
            movements = Movement.objects.filter(movement_name__icontains=query_term)
        else:
            movements = Movement.objects.all()

        html = render_to_string(
            template_name="wodmovements/movement-result-partial.html",
            context={"movements": movements}
        )

        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    if request.method == 'POST':
        components_form_set = ComponentsFormSet(request.POST)
        workout_form = WorkoutForm(request.POST)
        if components_form_set.is_valid() and workout_form.is_valid():
            workout: Workout = workout_form.save(commit=False)
            workout.creator = request.user.athlete
            workout.save()
            component_list = components_form_set.save()
            workout.components.set(component_list)
            workout.set_metadata()
            workout.save()
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
