from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from models import (
    Profile,
    Stand,
    StandRequest,
    StandContract,
    AdditionalService,
    ServiceRequest,
    Event,
    EventRequest,
    EventContract,
    AdditionalServiceCategory,
    AdditionalServiceSubcategory,
)


class ProfileAdmin(UserAdmin):
    model = Profile
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("address",)}),
    )


admin.site.register(Profile, ProfileAdmin)

admin.site.register(Stand)
admin.site.register(StandRequest)
admin.site.register(StandContract)

admin.site.register(AdditionalServiceCategory)
admin.site.register(AdditionalServiceSubcategory)
admin.site.register(AdditionalService)
admin.site.register(ServiceRequest)

admin.site.register(Event)
admin.site.register(EventRequest)
admin.site.register(EventContract)
