from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.urls import reverse


class Athlete(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('athletes:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"Athlete [ first_name: {self.first_name}, second_name: {self.last_name} ]"


