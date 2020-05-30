from django.db import models


class Athlete(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)

    def __str__(self):
        return f"Athlete [ first_Name: {self.first_name}, second_name: {self.second_name} ]"


class Workout(models.Model):
    workout_description = models.TextField(default='')
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return f"Workout [ workout_description: {self.workout_description}, athlete: {self.athlete}, " \
               f"date: {self.pub_date} ]"
