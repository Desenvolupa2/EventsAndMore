from django.contrib import admin

from .models import (
    Stand,
    StandRequest,
    StandContract,
    StandSize,
    AdditionalService,
    ServiceRequest,
    Event,
    EventRequest,
    EventContract,
)

# Register your models here.
admin.site.register(Stand)
admin.site.register(StandRequest)
admin.site.register(StandContract)

admin.site.register(AdditionalService)
admin.site.register(ServiceRequest)

admin.site.register(Event)
admin.site.register(EventRequest)
admin.site.register(EventContract)
