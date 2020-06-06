from django.forms import ModelForm, DateInput

from scores.models import Score


class ScoreForm(ModelForm):
    class Meta:
        model = Score
        fields = ['score', 'date', 'workout']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }
