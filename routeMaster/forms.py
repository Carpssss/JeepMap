# forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Route, Stop

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['route_id', 'route_name']


class StopForm(forms.ModelForm):
    class Meta:
        model = Stop
        fields = ['name', 'order']


StopFormSet = inlineformset_factory(Route, Stop, form=StopForm, extra=1, can_delete=True)
