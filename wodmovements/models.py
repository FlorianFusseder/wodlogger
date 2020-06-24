from django.db import models
from django.utils.translation import gettext_lazy as _


class Movement(models.Model):
    class Modality(models.TextChoices):
        GYMNASTIC = 'G', _('Gymnastics'),
        WEIGHTLIFTING = 'W', _('Wightlifiting'),
        MONOSTRUCTURAL = 'M', _("Monostructural")

    movement_name = models.CharField(max_length=50)
    has_weight = models.BooleanField()
    has_distance = models.BooleanField()
    has_height = models.BooleanField()
    modality = models.CharField(max_length=1,
                                choices=Modality.choices,
                                default=Modality.GYMNASTIC)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_movement_display(self):
        return self.movement_name

    def __str__(self):
        return f"Movement [ component_name: {self.movement_name}, modality: {self.modality} ]"


class Component(models.Model):
    reps = models.PositiveSmallIntegerField(blank=False, null=False, default=1)
    kg_a = models.PositiveSmallIntegerField(blank=True, null=True)
    kg_m = models.PositiveSmallIntegerField(blank=True, null=True)
    kg_f = models.PositiveSmallIntegerField(blank=True, null=True)
    distance = models.PositiveSmallIntegerField(blank=True, null=True)
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    timespan = models.DurationField(blank=True, null=True)
    movement = models.ForeignKey(Movement, on_delete=models.DO_NOTHING)

    def get_component_display(self):
        return f"{self.reps} {self.movement.get_movement_display()}"

    def __str__(self):
        return f"Component [ amount: {self.reps}, kg: {self.kg}, movement: {self.movement} ]"
