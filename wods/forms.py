from django.forms import ModelForm

from scores.forms import ScoreForm
from wods.models import Workout


class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'components', 'workout_style', 'description', 'workout_duration', 'rounds', 'rep_schema']


class AddScoreForm(ModelForm):
    class Meta(ScoreForm.Meta):
        pass
