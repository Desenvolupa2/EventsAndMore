from itertools import chain
from typing import Type

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.db.models import Model

from manager.models import (
    ServiceRequest,
    AdditionalService,
    StandRequest,
    EventRequest,
    Stand,
    Event
)


def get_permissions(model: Type['Model']):
    return list(chain.from_iterable(
        Permission.objects.filter(content_type=ContentType.objects.get_for_model(model))
    ))


GROUPS_PERMISSIONS = {
    "additional_services": list(chain(
        get_permissions(ServiceRequest),
        get_permissions(AdditionalService),
    )),
    "request_management": list(chain(
        get_permissions(StandRequest),
        get_permissions(Stand),
        get_permissions(EventRequest),
        get_permissions(Event),
    )),
}


class CreateGroupsPermissions(BaseCommand):

    def handle(self, *args, **options):
        for group_name, permissions in GROUPS_PERMISSIONS.items():
            group = Group.objects.create(name=group_name, permissions=permissions)
            group.save()
