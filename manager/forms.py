from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, EventRequest


class EventRequestForm(ModelForm):
    class Meta:
        model = EventRequest
        fields = ['event_name', 'initial_date', 'final_date']


class NewUserForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ("username", "email", "address", "password1", "password2")
