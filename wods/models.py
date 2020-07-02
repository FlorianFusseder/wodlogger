import django
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from athletes.models import Athlete
from wodmovements.models import Movement, Component


class Workout(models.Model):
    class WorkoutStyle(models.TextChoices):
        ROUNDS_FOR_TIME = 'RFT', _('Rounds for Time'),
        RFT_SAME_VARYING_REPS = 'RFT_SVR', _('RFT: Same Varying Reps (e.g. 21 - 15 - 9)'),
        RFT_INDEPENDENT_VARYING_REPS = 'RFT_IVR', _('RFT: Independent Varying Reps'),
        RFT_WITH_BOOKENDS = 'RFT_BOOK', _('RFT with Bookends (Buy-In, Buy-Out)'),
        EACH_ROUND_FOR_TIME = 'ERFT', _('Each Round For Time'),
        FOR_TIME = 'FT', _('For Time'),
        FOR_QUALITY = 'FQ', _('For Quality'),
        EMOM_MULTIPLE_MOVEMENTS_PER_INTERVAL = 'EMOM_M', _('EMOM: Multiple Movements per Interval'),
        EMOM_ALTERNATE_MOVEMENTS_EACH_INTERVAL = 'EMOM_A', _('EMOM: Alternate Movements each Interval'),
        AMRAP = 'AMRAP', _('AMRAP'),
        AMRAP_REPEATS = 'AMRAP_R', _('AMRAP Repeats'),
        AMRAP_WITH_BUY_IN = 'AMRAP_BI', _('AMRAP with Buy-In'),
        AMRAP_WITH_MAX_REP = 'AMRAP_MR', _('AMRAP with Max Rep'),
        AMREPS = 'AMREPS', _('AMReps'),
        ASCENDING_AMREPS = 'ASC_AMREPS', _('Ascending AMReps'),
        TABATA = 'T', _('Tabata'),
        FGB_STYLE = 'FGB', _('FGB Style'),
        DEATH_BY_REPS = 'DBR', _('Death By Reps'),
        ROUNDS_FOR_MAX_REPS = 'RFMR', _('Rounds for Max Reps'),
        REPS_IN_REMAINING_TIME = 'RRT', _('Reps in Remaining Time'),

        SETS = 'SETS', ('Sets'),
        EMOM = 'EMOM', _('EMOM'),
        X_REPS_FOR_TIME = 'X_RFT', _('X Reps for Time'),
        AMREPS_IN_X_TIME = 'AIXT', _('AMReps in X Time'),
        MAX_DURATION = 'MD', _('Max Duration'),
        X_REP_MAX = 'RM', _('X Rep Max'),
        DEATH_BY_WEIGHT = 'DBW', _('Death By Weight'),
        SINGLE_DISTANCE = 'SD', _('Single Distance'),
        INTERVALS_REPEATS = 'IR', _('Intervals / Repeats'),
        DEATH_BY_DISTANCE = 'DBD', _('Death By Distance'),
        ON_THE_MINUTE = 'OTM', _('On the Minute'),
        FOR_DISTANCE = 'FD', _('For Distance'),

    class WorkoutType(models.TextChoices):
        TIMED = 'TIMED', _('Timed'),
        AS_MANY_ROUNDS_AS_POSSIBLE = 'AMRAP', _('AMRAP'),
        TABATA = 'TABATA', _('Tabata'),
        TOTAL_REPS = 'TOTAL_REPS', _('Total Reps')

    class BenchMark(models.TextChoices):
        GIRL = 'GIRL', _('Girl'),
        LIFT = 'LIFT', _('Lift'),
        HERO = 'HERO', _('Hero'),
        ENDURANCE = 'ENDURANCE', _('Endurance'),
        GYMNASTIC = 'GYMNASTIC', _('Gymnastic'),
        THE_OPEN = 'THE_OPEN', _('The Open'),
        FAMOUS = 'FAMOUS', _('Famous'),

    class Scheme(models.TextChoices):
        SINGLET = 'SINGLET', _('Singlet'),
        COUPLET = 'COUPLET', _('Couplet'),
        TRIPLET = 'TRIPLET', _('Triplet'),
        CHIPPER = 'CHIPPER', _('Chipper'),
        MULTLET = 'MULTLET', _('MULTLET'),

    class RepetitionCount(models.TextChoices):
        LOW = 'L', _('Low'),
        MEDIUM = 'M', _('Medium'),
        HIGH = 'H', _('High')

    class Duration(models.TextChoices):
        SPRINT = 'SPRINT', _('Sprint'),
        SHORT = 'SHORT', _('Short'),
        MEDIUM = 'MEDIUM', _('Medium'),
        LONG = 'LONG', _('Long')

    class Load(models.TextChoices):
        LIGHT = 'L', _('Light'),
        MEDIUM = 'M', _('Medium'),
        HEAVY = 'H', _('Heavy')

    class Modality(models.TextChoices):
        METCON = 'M', _('Metcon'),
        GYMNASTIC = 'G', _('Gymnastic'),
        WEIGHTLIFTING = 'W', _('Weightlifting')
        METCON_GYMNASTIC = 'MG', _('Metcon and Gymnastic')
        METCON_WEIGHTLIFTING = 'MW', _('Metcon and Weightlifting')
        WEIGHTLIFTING_GYMNASTIC = 'WG', _('Weightlifting and Gymnastic')

    name = models.CharField(max_length=200)
    components = models.ManyToManyField(Component)
    description = models.TextField(default='', blank=True)
    creator = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    date = models.DateTimeField(default=django.utils.timezone.now)

    workout_style = models.CharField(max_length=10, choices=WorkoutStyle.choices)
    workout_duration = models.DurationField(blank=True, null=True)
    rounds = models.PositiveSmallIntegerField(blank=True, null=True)
    rep_schema = models.CharField(max_length=50, blank=True)

    workout_type = models.CharField(max_length=10, choices=WorkoutType.choices, blank=True)
    benchmark = models.CharField(max_length=10, choices=BenchMark.choices, blank=True)
    scheme = models.CharField(max_length=7, choices=Scheme.choices, blank=True)
    repetition_count = models.CharField(max_length=1, choices=RepetitionCount.choices, blank=True)
    duration = models.CharField(max_length=6, choices=Duration.choices, blank=True)
    load = models.CharField(max_length=1, choices=Load.choices, blank=True)
    modality = models.CharField(max_length=3, choices=Modality.choices, blank=True)

    def get_absolute_url(self):
        return reverse('wods:detail', kwargs={'pk': self.pk})

    def get_components(self):
        return Component.objects.filter(workout__pk=self.pk)

    def get_components_display(self):
        return "\n".join([x.get_component_display() for x in self.get_components()])

    def set_metadata(self):
        pass

    def __str__(self):
        return f"Workout [ name: {self.name}, workout_description: {self.description}, type: {self.workout_type}" \
               f" athlete: {self.creator}, date: {self.date} ]"
