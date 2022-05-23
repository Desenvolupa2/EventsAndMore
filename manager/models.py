import uuid as uuid
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Profile(AbstractUser):
    nif = models.CharField(max_length=9)
    address = models.CharField(max_length=100)


class PhoneNumber(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    prefix = models.PositiveIntegerField()
    number = models.PositiveIntegerField()


class EventRequestStatus(models.IntegerChoices):
    PENDING_ON_MANAGER = 1
    PENDING_ON_ORGANIZER = 2
    ACCEPTED = 3
    DENIED = 4


class EventRequest(models.Model):
    entity = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    initial_date = models.DateField()
    final_date = models.DateField()
    status = models.IntegerField(choices=EventRequestStatus.choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def status_name(self) -> str:
        return " ".join(EventRequestStatus(self.status).name.split("_"))

    @property
    def has_conflicts(self) -> bool:
        self_stand_requests = EventRequestStand.objects.filter(event_request=self)
        for event_request in EventRequest.objects.filter(status=EventRequestStatus.ACCEPTED):
            event_stand_requests = EventRequestStand.objects.filter(event_request=event_request)
            if (
                    event_request != self and
                    (event_request.initial_date <= self.initial_date <= event_request.final_date or
                     event_request.initial_date <= self.final_date <= event_request.final_date) and
                    any(e.stand in (er.stand for er in event_stand_requests) for e in self_stand_requests)
            ):
                return True
        return False

    @property
    def related_event(self) -> 'Event':
        contract = EventContract.objects.get(event_request=self)
        return contract.event


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    initial_date = models.DateField()
    final_date = models.DateField()
    status = models.BooleanField(default=True)
    image = models.ImageField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class EventContract(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_request = models.ForeignKey(EventRequest, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    file = models.FileField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class EventInvoice(models.Model):
    event_request = models.ForeignKey(EventRequest, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    file = models.FileField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ReservationStatus(models.IntegerChoices):
    DELETED = 0
    PENDING = 1
    CONFIRMED = 2


class Reservation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    initial_date = models.DateField()
    final_date = models.DateField()
    status = models.IntegerField(choices=ReservationStatus.choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ReservationContract(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Profile, on_delete=models.CASCADE)
    booking = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    file = models.FileField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ReservationInvoice(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    file = models.FileField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Stand(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class GridPosition(models.Model):
    x_position = models.IntegerField()
    y_position = models.IntegerField()
    stand = models.ForeignKey(Stand, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class StandReservation(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class EventRequestStand(models.Model):
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE)
    event_request = models.ForeignKey(EventRequest, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Catalog(models.Model):
    name = models.CharField(default=f"Catàleg", max_length=100)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class AdditionalServiceCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AdditionalServiceSubcategory(models.Model):
    category = models.ForeignKey(AdditionalServiceCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class AdditionalService(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    subcategory = models.ForeignKey(AdditionalServiceSubcategory, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    image = models.ImageField()
    status = models.BooleanField(default=False)
    taxes = models.DecimalField(
        decimal_places=2,
        max_digits=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )


class AdditionalServiceReservation(models.Model):
    stand_reservation = models.ForeignKey(StandReservation, on_delete=models.CASCADE)
    additional_service = models.ForeignKey(AdditionalService, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(AdditionalServiceSubcategory, on_delete=models.CASCADE)
    initial_date = models.DateField()
    final_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
