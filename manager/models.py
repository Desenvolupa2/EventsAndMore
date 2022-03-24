from django.db import models


class Event(models.Model):
    name = None
    initial_date = None
    final_date = None


class EventContract(models.Model):
    file = None


class Stand(models.Model):
    size = None


class StandContract(models.Model):
    entity = None
    stand = None
    file = None


class AdditionalService(models.Model):
    name = None
    price = None


class EventRequest(models.Model):
    name = None
    initial_date = None
    final_date = None
    status = None


class StandRequest(models.Model):
    entity = None
    event = None
    stand = None
    initial_date = None
    final_date = None


class ServiceRequest(models.Model):
    entity = None
    stand = None
    service = None
    event = None

# TODO: user groups and permissions
