from django.db import models
from django.urls import reverse

from athletes.models import Athlete


class Workout(models.Model):
    description = models.TextField(default='')
    score_type = models.CharField(max_length=50,
                                  choices=[
                                      ('FOR_TIME', 'For Time'),
                                      ('AMRAP', 'AMRAP'),
                                      ('EMOM', 'EMOM'),
                                      ('LIFTING', 'Weightlifting'),
                                      ('REPS_SETS', 'Reps and Sets')
                                  ],
                                  default='FOR_TIME')
    score = models.CharField(max_length=50)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    date = models.DateField()

    def get_absolute_url(self):
        return reverse('wods:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"Workout [ workout_description: {self.description}, athlete: {self.athlete}, date: {self.date} ]"
