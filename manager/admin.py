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


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("address",)}),
    )


admin.site.register(User, CustomUserAdmin)

admin.site.register(Stand)
admin.site.register(StandRequest)
admin.site.register(StandContract)

admin.site.register(AdditionalService)
admin.site.register(ServiceRequest)

admin.site.register(Event)
admin.site.register(EventRequest)
admin.site.register(EventContract)
