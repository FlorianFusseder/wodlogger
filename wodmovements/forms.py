from django.forms import ModelForm, ModelChoiceField

from wodmovements.models import Component


class MovementModelChoiceField(ModelChoiceField):
    def __init__(self, queryset, *, empty_label="Select a movement", required=True, widget=None, label=None,
                 initial=None,
                 help_text='', to_field_name=None, limit_choices_to=None, **kwargs):
        super().__init__(queryset, empty_label=empty_label, required=required, widget=widget, label=label,
                         initial=initial, help_text=help_text, to_field_name=to_field_name,
                         limit_choices_to=limit_choices_to, **kwargs)

    def label_from_instance(self, obj):
        return obj.get_movement_display()


class ComponentForm(ModelForm):
    class Meta:
        model = Component
        fields = ['reps', 'movement']
        field_classes = {
            'movement': MovementModelChoiceField
        }
