from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from manager.models import (
    EventRequest,
    Profile,
    ServiceCategory,
    AdditionalService,
    ServiceSubcategory,
)


class NewUserForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ("username", "email", "address", "password1", "password2")


class DateInput(forms.DateInput):
    input_type = 'date'


class EventRequestForm(ModelForm):
    class Meta:
        model = EventRequest
        fields = ['name', 'initial_date', 'final_date']
        widgets = {
            'initial_date': DateInput(),
            'final_date': DateInput()
        }


class AdditionalServiceCategoryForm(ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ['name']


class AdditionalServiceSubcategoryForm(ModelForm):
    class Meta:
        model = ServiceSubcategory
        fields = '__all__'


class AdditionalServiceForm(ModelForm):
    class Meta:
        model = AdditionalService
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = ServiceSubcategory.objects.none()

        if 'subcategory' in self.data:
            category_id = int(self.data.get('category'))
            self.fields['subcategory'].queryset = ServiceSubcategory.objects.filter(
                belongs_to_id=category_id).order_by('name')

        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('name')
