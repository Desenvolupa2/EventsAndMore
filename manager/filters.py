import django_filters

from manager.models import EventRequestStatus, EventRequest


class EventRequestsFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=EventRequestStatus.choices)

    class Meta:
        model = EventRequest
        fields = ['status']
