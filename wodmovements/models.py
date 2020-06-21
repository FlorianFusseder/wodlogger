from django.db import models
from django.utils.translation import gettext_lazy as _


class Movement(models.Model):
    class Modality(models.TextChoices):
        GYMNASTIC = 'G', _('Gymnastics'),
        WEIGHTLIFTING = 'W', _('Wightlifiting'),
        MONOSTRUCTURAL = 'M', _("Monostructural")

    class Unit(models.TextChoices):
        METERS = 'METERS', _("Meters"),
        REPETITIONS = 'REPS', _("Reps"),
        WEIGHT = 'WEIGHT', _("kg")
        REPETITIONS_AND_WEIGHT = 'REPS_AND_WEIGHT', _("Reps @ kg")
        CALORIES = 'CALORIES', _("Calories")

    movement_name = models.CharField(max_length=50)
    movement_unit = models.CharField(max_length=20,
                                     choices=Unit.choices,
                                     default=Unit.REPETITIONS)
    modality = models.CharField(max_length=1,
                                choices=Modality.choices,
                                default=Modality.GYMNASTIC)

    def __str__(self):
        return f"Movement [ component_name: {self.movement_name}, component_unit: {self.movement_unit}, " \
               f"modality: {self.modality} ]"
