from itertools import chain
from typing import Type

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.db.models import Model

from manager.models import (
    EventRequest,
    Event,
    Stand,
    AdditionalService,
    ServiceCategory,
    ServiceSubcategory,
)


def get_permissions(model: Type['Model']):
    return Permission.objects.filter(content_type=ContentType.objects.get_for_model(model))


GROUPS_PERMISSIONS = {
    "Additional services": chain(
        get_permissions(AdditionalService),
        get_permissions(ServiceCategory),
        get_permissions(ServiceSubcategory),
    ),

    "Request management": chain(
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
