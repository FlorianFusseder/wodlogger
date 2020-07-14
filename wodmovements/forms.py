from django.forms import CharField, Form, IntegerField, DecimalField


class ComponentForm(Form):
    reps = IntegerField(initial=1)
    movement = CharField(max_length=50, initial='placeholder-string')
    kg = DecimalField(initial=0.0, decimal_places=2)
    distance = DecimalField(initial=0.0, decimal_places=2)
    height = DecimalField(initial=0.0, decimal_places=2)
