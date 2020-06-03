from django.forms import ModelForm, DateInput

from wods.models import Workout


class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['workout_description', 'athlete', 'pub_date', ]
        widgets = {
            'pub_date': DateInput(attrs={'type': 'date'}),
        }
