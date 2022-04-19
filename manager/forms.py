from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from .models import EventRequest, User


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "address", "password1", "password2")


class DateInput(forms.DateInput):
    input_type = 'date'


class EventRequestForm(ModelForm):
    class Meta:
        model = EventRequest
        fields = ['event_name', 'initial_date', 'final_date']
        widgets = {
            'initial_date': DateInput(),
            'final_date': DateInput()
        }
