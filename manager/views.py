from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, TemplateView, FormView, ListView
from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, ListView

from manager.forms import EventRequestForm
from manager.models import EventRequest, EventRequestStatus

from manager.forms import NewUserForm


class Home(TemplateView):
    template_name = "home.html"


class Register(CreateView):
    form_class = NewUserForm
    template_name = "register.html"

    def get_success_url(self):
        return reverse_lazy("home")


class Login(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        return reverse_lazy('home')


class EventRequestFormView(LoginRequiredMixin, FormView):
    template_name = "event_request_form.html"
    form_class = EventRequestForm

    def form_valid(self, form):
        event_request: 'EventRequest' = form.save(commit=False)
        event_request.entity = self.request.user
        event_request.status = EventRequestStatus.PENDING
        event_request.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("home")


class EventRequestListView(LoginRequiredMixin, ListView):
    template_name = "event_request_list.html"
    context_object_name = "events"
    model = EventRequest
    paginate_by = 10
    ordering = "initial_date"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["all_status"] = EventRequestStatus.choices
        return context


class EventRequestStatusUpdate(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        event_request = EventRequest.objects.get(id=pk)
        if event_request is None:
            return HttpResponse("Invalid pk", status=HTTPStatus.BAD_REQUEST)

        status = kwargs.get('status')
        if status is None:
            return HttpResponse("Invalid status", status=HTTPStatus.BAD_REQUEST)

        event_request.status = EventRequestStatus(status)
        event_request.save()
        return HttpResponseRedirect(reverse_lazy("event-request-list"))
