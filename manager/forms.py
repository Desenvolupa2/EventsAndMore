from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from manager.models import EventRequest, Profile, AdditionalServiceCategory, AdditionalService, \
    AdditionalServiceSubcategory


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


class AdditionalServiceCategoryForm(ModelForm):
    class Meta:
        model = AdditionalServiceCategory
        fields = ['name']


class AdditionalServiceSubcategoryForm(ModelForm):
    class Meta:
        model = AdditionalServiceSubcategory
        fields = ['name', 'belongs_to']


class AdditionalServiceForm(ModelForm):
    class Meta:
        model = AdditionalService
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = AdditionalServiceSubcategory.objects.none()

        if 'subcategory' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = AdditionalServiceSubcategory.objects.filter(
                    belongs_to_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('name')
