from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Profile,
    PhoneNumber,
    EventRequest,
    Event,
    EventContract,
    EventInvoice,
    Reservation,
    ReservationContract,
    ReservationInvoice,
    Stand,
    GridPosition,
    StandReservation,
    Catalog,
    AdditionalService,
    AdditionalServiceCategory,
    AdditionalServiceSubcategory,
    AdditionalServiceReservation,
)


class ProfileAdmin(UserAdmin):
    model = Profile
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("address",)}),
    )


admin.site.register(Profile, ProfileAdmin)
admin.site.register(PhoneNumber)

admin.site.register(Event)
admin.site.register(EventRequest)
admin.site.register(EventContract)
admin.site.register(EventInvoice)

admin.site.register(Reservation)
admin.site.register(ReservationContract)
admin.site.register(ReservationInvoice)

admin.site.register(Stand)
admin.site.register(GridPosition)
admin.site.register(StandReservation)

admin.site.register(Catalog)
admin.site.register(AdditionalService)
admin.site.register(AdditionalServiceCategory)
admin.site.register(AdditionalServiceSubcategory)
admin.site.register(AdditionalServiceReservation)
