from django.forms import CharField, Form, IntegerField


class ComponentForm(Form):
    reps = IntegerField(initial=1)
    movement = CharField(max_length=50, initial='placeholder-string')
