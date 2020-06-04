from django.forms import ModelForm

from athletes.models import Athlete


class AthleteForm(ModelForm):
    class Meta:
        model = Athlete
        fields = '__all__'
