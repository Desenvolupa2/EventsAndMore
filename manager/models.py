from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    initial_date = models.DateField()
    final_date = models.DateField()


class EventContract(models.Model):
    file = models.FileField()


class StandSize(models.IntegerChoices):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Stand(models.Model):
    size = models.IntegerField(choices=StandSize.choices)


class StandContract(models.Model):
    entity = models.ForeignKey(User, on_delete=models.SET_NULL)
    stand = models.ForeignKey(Stand, on_delete=models.SET_NULL)
    file = models.FileField()


class AdditionalService(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2)


class EventRequest(models.Model):
    event_name = models.CharField(max_length=100)
    initial_date = models.DateField()
    final_date = models.DateField()
    status = models.BooleanField()


class StandRequest(models.Model):
    entity = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE)
    initial_date = models.DateField()
    final_date = models.DateField()


class ServiceRequest(models.Model):
    entity = models.ForeignKey(User, on_delete=models.CASCADE)
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE)
    service = models.ForeignKey(AdditionalService, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

# TODO: user groups and permissions
