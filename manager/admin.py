from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    Stand,
    StandRequest,
    StandContract,
    AdditionalService,
    ServiceRequest,
    Event,
    EventRequest,
    EventContract,
)

admin.site.register(User, UserAdmin)

admin.site.register(Stand)
admin.site.register(StandRequest)
admin.site.register(StandContract)

admin.site.register(AdditionalService)
admin.site.register(ServiceRequest)

admin.site.register(Event)
admin.site.register(EventRequest)
admin.site.register(EventContract)
