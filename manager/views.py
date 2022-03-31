from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView

from manager.forms import EventRequestForm
from manager.models import EventRequest, EventRequestStatus


class Home(TemplateView):
    template_name = "home.html"


class EventRequestView(LoginRequiredMixin, FormView):
    template_name = "event_request.html"
    form_class = EventRequestForm

    def form_valid(self, form):
        event_request: 'EventRequest' = form.save(commit=False)
        event_request.entity = self.request.user
        event_request.status = EventRequestStatus.PENDING
        event_request.save()
        return HttpResponseRedirect(self.get_success_url())
