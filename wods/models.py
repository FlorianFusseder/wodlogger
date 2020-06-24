import django
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from athletes.models import Athlete
from wodmovements.models import Movement, Component


class Workout(models.Model):
    class WorkoutType(models.TextChoices):
        FOR_TIME = 'FOR_TIME', _('For Time'),
        AS_MANY_REPETITIONS_AS_POSSIBLE = 'AMRAP', _('AMRAP'),
        EVERY_MINUTE_ON_THE_MINUTE = 'EMOM', _('EMOM'),
        WEIGHTLIFTING = 'LIFTING', _('Weightlifting'),
        REPS_AND_SETS = 'REPSCHEME', _('Rep Scheme')

    name = models.CharField(max_length=200)
    components = models.ManyToManyField(Component)
    description = models.TextField(default='', blank=True)
    creator = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    date = models.DateTimeField(default=django.utils.timezone.now)
    workout_type = models.CharField(max_length=9,
                                    choices=WorkoutType.choices,
                                    default=WorkoutType.FOR_TIME)

    def get_absolute_url(self):
        return reverse('wods:detail', kwargs={'pk': self.pk})

    def get_components(self):
        return Component.objects.filter(workout__pk=self.pk)

    def get_components_display(self):
        return "\n".join([x.get_component_display() for x in self.get_components()])

    def __str__(self):
        return f"Workout [ name: {self.name}, workout_description: {self.description}, type: {self.workout_type}" \
               f" athlete: {self.creator}, date: {self.date} ]"
