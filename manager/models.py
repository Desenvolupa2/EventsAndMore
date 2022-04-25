from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify


class Profile(AbstractUser):
    address = models.CharField(max_length=150, blank=True, null=False)
    # TODO: add all the required fields


class Event(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    initial_date = models.DateField()
    final_date = models.DateField()


class EventContract(models.Model):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    entity = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    file = models.FileField()


class StandSize(models.IntegerChoices):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Stand(models.Model):
    size = models.IntegerField(choices=StandSize.choices)


class StandContract(models.Model):
    entity = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    stand = models.ForeignKey(Stand, on_delete=models.SET_NULL, null=True)
    file = models.FileField()


class AdditionalServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AdditionalServiceSubcategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    belongs_to = models.ForeignKey(AdditionalServiceCategory, on_delete=models.CASCADE)
    slug = models.SlugField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AdditionalService(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=9999, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    taxes = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(AdditionalServiceCategory, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(AdditionalServiceSubcategory, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='uploads/')
    slug = models.SlugField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class EventRequestStatus(models.IntegerChoices):
    PENDING = 1
    ACCEPTED = 2
    DENIED = 3


class EventRequest(models.Model):
    entity = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    initial_date = models.DateField()
    final_date = models.DateField()
    status = models.IntegerField(choices=EventRequestStatus.choices)

    @property
    def status_name(self):
        return EventRequestStatus(self.status).name


class StandRequest(models.Model):
    entity = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE)
    initial_date = models.DateField()
    final_date = models.DateField()


class ServiceRequest(models.Model):
    entity = models.ForeignKey(Profile, on_delete=models.CASCADE)
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE)
    service = models.ForeignKey(AdditionalService, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
