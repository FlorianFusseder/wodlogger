from django.db import models
from django.utils.translation import gettext_lazy as _


class Movement(models.Model):
    class Modality(models.TextChoices):
        GYMNASTIC = 'G', _('Gymnastics'),
        WEIGHTLIFTING = 'W', _('Wightlifiting'),
        MONOSTRUCTURAL = 'M', _("Monostructural")

    class Unit(models.TextChoices):
        METERS = 'METERS', _("m"),
        REPETITIONS = 'REPS', _("x"),
        WEIGHT = 'WEIGHT', _("kg")
        REPETITIONS_AND_WEIGHT = 'REPS_AND_WEIGHT', _("x @ kg")
        CALORIES = 'CALORIES', _("cal")

    movement_name = models.CharField(max_length=50)
    movement_unit = models.CharField(max_length=20,
                                     choices=Unit.choices,
                                     default=Unit.REPETITIONS)
    modality = models.CharField(max_length=1,
                                choices=Modality.choices,
                                default=Modality.GYMNASTIC)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_movement_display(self):
        return self.movement_name

    def get_unit_display(self):
        return dict(Movement.Unit.choices)[self.movement_unit]

    def __str__(self):
        return f"Movement [ component_name: {self.movement_name}, component_unit: {self.movement_unit}, " \
               f"modality: {self.modality} ]"
