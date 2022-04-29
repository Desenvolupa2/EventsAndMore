from itertools import chain
from typing import Type

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.db.models import Model

from manager.models import (
    StandRequest,
    EventRequest,
    Stand,
    Event,
    ServiceRequest,
    AdditionalService,
    AdditionalServiceSubcategory,
    AdditionalServiceCategory
)


def get_permissions(model: Type['Model']):
    return Permission.objects.filter(content_type=ContentType.objects.get_for_model(model))


GROUPS_PERMISSIONS = {
    "Additional services": chain(
        get_permissions(ServiceRequest),
        get_permissions(AdditionalService),
        get_permissions(AdditionalServiceCategory),
        get_permissions(AdditionalServiceSubcategory),
    ),

    "Request management": chain(
        get_permissions(StandRequest),
        get_permissions(Stand),
        get_permissions(EventRequest),
        get_permissions(Event),
    ),
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        for group_name, permissions in GROUPS_PERMISSIONS.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            group.permissions.add(*permissions)
            group.save()
