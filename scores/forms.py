from django.forms import ModelForm, DateInput

from scores.models import Score


class ScoreForm(ModelForm):
    class Meta:
        model = Score
        fields = ['score', 'execution_date', 'comment']
        widgets = {
            'execution_date': DateInput(attrs={'type': 'date'}),
        }
