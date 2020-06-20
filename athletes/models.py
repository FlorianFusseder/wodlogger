from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Athlete(models.Model):
    class Sex(models.TextChoices):
        MALE = 'M', _('Male'),
        FEMALE = 'F', _('Female'),
        PRIVATE = 'X', _("I don't want to share")

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=1,
                           choices=Sex.choices,
                           default=Sex.PRIVATE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_signature(self):
        if self.last_name and self.first_name:
            return f"{self.last_name}, {self.first_name}"
        return f"{self.user.username}"

    def get_absolute_url(self):
        return reverse('athletes:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"Athlete [ first_name: {self.first_name}, second_name: {self.last_name} ]"
