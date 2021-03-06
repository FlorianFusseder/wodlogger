from django.db import models
from django.utils.translation import gettext_lazy as _


class Movement(models.Model):
    class Modality(models.TextChoices):
        GYMNASTIC = 'G', _('Gymnastics'),
        WEIGHTLIFTING = 'W', _('Weightlifting'),
        MONOSTRUCTURAL = 'M', _("Monostructural")

    movement_name = models.CharField(max_length=50)
    has_reps = models.BooleanField()
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
        return f"Movement [ movement_name: {self.movement_name}, modality: {self.modality} ]"


class Component(models.Model):
    reps = models.PositiveSmallIntegerField(blank=False, null=False, default=1)
    max_reps = models.BooleanField(default=False)
    kg_m = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=2)
    kg_f = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=2)
    distance = models.PositiveSmallIntegerField(blank=True, null=True)
    height = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=3)
    timespan = models.DurationField(blank=True, null=True)
    movement = models.ForeignKey(Movement, on_delete=models.DO_NOTHING)

    def get_component_display(self):
        return f"{self.reps} {self.movement.get_movement_display()}"

    def get_movement_display(self):
        return self.movement.get_movement_display()

    def __str__(self):
        return f"Component [ amount: {self.reps}, kg: {self.kg_f}/{self.kg_m}, movement: {self.movement} ]"
