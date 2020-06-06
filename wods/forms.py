from django.forms import ModelForm

from scores.forms import ScoreForm
from scores.models import Score
from wods.models import Workout


class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['description', 'type']


class AddScoreForm(ModelForm):
    class Meta(ScoreForm.Meta):
        model = Score
        fields = ['score', 'execution_date']
