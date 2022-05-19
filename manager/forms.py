from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from manager.models import (
    AdditionalService,
    AdditionalServiceCategory,
    AdditionalServiceSubcategory,
    EventRequest,
    Profile,
    Catalog,
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
        model = AdditionalServiceCategory
        fields = ['name']


class AdditionalServiceSubcategoryForm(ModelForm):
    class Meta:
        model = AdditionalServiceSubcategory
        fields = '__all__'


class CatalogForm(ModelForm):
    class Meta:
        model = Catalog
        fields = ['name']


class AdditionalServiceForm(ModelForm):
    category = forms.ModelChoiceField(queryset=AdditionalServiceCategory.objects.all())

    class Meta:
        model = AdditionalService
        fields = ('catalog', 'name', 'category', 'subcategory', 'price', 'taxes', 'image', 'status')
        labels = {
            'status': 'Service available from this moment:'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = AdditionalServiceSubcategory.objects.none()

        if 'subcategory' in self.data:
            category_id = int(self.data.get('category'))
            self.fields['subcategory'].queryset = AdditionalServiceSubcategory.objects.filter(
                category=category_id).order_by('name')

        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('name')
