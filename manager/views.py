from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from manager.forms import NewUserForm


class Home(TemplateView):
    template_name = "home.html"


class Register(FormView):
    form_class = NewUserForm
    template_name = "register.html"

    def get_success_url(self):
        return reverse_lazy("home")


class Login(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        return reverse_lazy('home')
