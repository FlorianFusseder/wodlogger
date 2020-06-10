import django
from django.db import models
from django.urls import reverse

from athletes.models import Athlete


class Workout(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default='')
    creator = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    date = models.DateTimeField(default=django.utils.timezone.now)
    type = models.CharField(max_length=50,
                            choices=[
                                ('FOR_TIME', 'For Time'),
                                ('AMRAP', 'AMRAP'),
                                ('EMOM', 'EMOM'),
                                ('LIFTING', 'Weightlifting'),
                                ('REPS_SETS', 'Reps and Sets')
                            ],
                            default='FOR_TIME')

    def get_absolute_url(self):
        return reverse('wods:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"Workout [ name: {self.name}, workout_description: {self.description}, type: {self.type} athlete: {self.creator}, date: {self.date} ]"
