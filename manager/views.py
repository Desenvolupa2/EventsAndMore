import json

from django.contrib.auth.views import LoginView
from django.core import serializers
from django.views.generic import CreateView, TemplateView, FormView, ListView
from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View

from manager.forms import EventRequestForm
from manager.models import EventRequest, EventRequestStatus
from django.forms.models import model_to_dict

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
    redirect_authenticated_user = True

    def get_redirect_url(self):
        return reverse_lazy("home")

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


class EventRequestUpdate(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)

    def put(self, *args, **kwargs):
        if not self.request.user.has_perm("change_event_request"):
            return JsonResponse({"status": "error", "content": "You have no permissions"}, status=HTTPStatus.FORBIDDEN)

        pk = kwargs.get('pk')
        event_request = EventRequest.objects.get(id=pk)
        if event_request is None:
            return JsonResponse({"status": "error", "content": "Invalid pk"}, status=HTTPStatus.BAD_REQUEST)

        if event_request.status != EventRequestStatus.PENDING:
            return JsonResponse(
                {"status": "error", "content": "This request can't be updated"},
                status=HTTPStatus.BAD_REQUEST
            )
        body = json.loads(self.request.body)
        for key, value in body.items():
            if hasattr(event_request, key):
                setattr(event_request, key, value)
            else:
                return JsonResponse({"status": "error", "content": "Invalid format"}, status=HTTPStatus.BAD_REQUEST)

        event_request.save()
        return JsonResponse({"status": "success", "content": model_to_dict(event_request)}, status=HTTPStatus.OK)
