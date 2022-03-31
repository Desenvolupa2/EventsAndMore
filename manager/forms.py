from django.forms import ModelForm

from manager.models import EventRequest


class EventRequestForm(ModelForm):

    class Meta:
        model = EventRequest
        fields = ['event_name', 'initial_date', 'final_date']
