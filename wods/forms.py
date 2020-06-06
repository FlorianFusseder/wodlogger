from django.forms import ModelForm, DateInput

from wods.models import Workout


class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['description', 'type']
