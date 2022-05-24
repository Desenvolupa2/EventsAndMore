import django_filters

from manager.models import EventRequest, EventRequestStatus


class EventRequestsFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.form.fields['status'].widget.attrs.update({'class': 'form-control'})

    status = django_filters.ChoiceFilter(choices=EventRequestStatus.choices)

    class Meta:
        model = EventRequest
        fields = ['status']
