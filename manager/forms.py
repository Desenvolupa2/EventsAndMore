from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from manager.models import EventRequest, Profile, AdditionalServiceCategory, AdditionalService, AdditionalServiceSubcategory


class NewUserForm(UserCreationForm):
    class Meta:
        model = Profile
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


class AdditionalServiceForm(ModelForm):
    class Meta:
        model = AdditionalService
        fields = ['name', 'description', 'price', 'taxes', 'category', 'subcategory', 'picture']


class AdditionalServiceCategoryForm(ModelForm):
    class Meta:
        model = AdditionalServiceCategory
        fields = ['name']


class AdditionalServiceSubcategoryForm(ModelForm):
    class Meta:
        model = AdditionalServiceSubcategory
        fields = ['name', 'belongs_to']

