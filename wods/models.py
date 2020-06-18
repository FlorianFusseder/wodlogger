import django
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from athletes.models import Athlete


class Workout(models.Model):
    class WorkoutType(models.TextChoices):
        FOR_TIME = 'FOR_TIME', _('For Time'),
        AS_MANY_REPETITIONS_AS_POSSIBLE = 'AMRAP', _('AMRAP'),
        EVERY_MINUTE_ON_THE_MINUTE = 'EMOM', _('EMOM'),
        WEIGHTLIFTING = 'LIFTING', _('Weightlifting'),
        REPS_AND_SETS = 'REPS_SETS', _('Reps and Sets')

    name = models.CharField(max_length=200)
    description = models.TextField(default='')
    creator = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    date = models.DateTimeField(default=django.utils.timezone.now)
    workout_type = models.CharField(max_length=9,
                                    choices=WorkoutType.choices,
                                    default=WorkoutType.FOR_TIME)

    def get_absolute_url(self):
        return reverse('wods:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"Workout [ name: {self.name}, workout_description: {self.description}, type: {self.workout_type} athlete: {self.creator}, date: {self.date} ]"
