from django.contrib.auth.forms import UserCreationForm

from .models import User


class NewUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "address", "password1", "password2")
