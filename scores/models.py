from django.db import models
from django.urls import reverse

from athletes.models import Athlete
from wods.models import Workout


class Score(models.Model):
    score = models.CharField(max_length=50)
    date = models.DateField()
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('score:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"Score [ {self.workout} score_type: {self.type}, score: {self.score}, date: {self.date} ]"
