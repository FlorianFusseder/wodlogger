from django.db import models
from django.urls import reverse

from athletes.models import Athlete


class Workout(models.Model):
    workout_description = models.TextField(default='')
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')

    def get_absolute_url(self):
        return reverse('wods:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"Workout [ workout_description: {self.workout_description}, athlete: {self.athlete}, " \
               f"date: {self.pub_date} ]"
