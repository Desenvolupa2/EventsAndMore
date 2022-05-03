import json
from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import SuspiciousOperation
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, FormView, ListView, DeleteView

from manager.forms import EventRequestForm, AdditionalServiceCategoryForm, NewUserForm, \
    AdditionalServiceSubcategoryForm, AdditionalServiceForm
from manager.models import EventRequest, EventRequestStatus, AdditionalService, AdditionalServiceCategory, \
    AdditionalServiceSubcategory


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
        if not self.request.user.is_superuser:
            context["events"] = context["events"].filter(user=self.request.user)
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


# Add categories
class AdditionalServiceCategoryCreateView(CreateView):
    context = {}
    template_name = 'service_category_form.html'
    form_class = AdditionalServiceCategoryForm

    def get_context_data(self, **kwargs):
        context = super(AdditionalServiceCategoryCreateView, self).get_context_data(**kwargs)
        context['categories'] = AdditionalServiceCategory.objects.all()
        return context

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        if self.request.user.has_perm('manager.add_additionalservicecategory'):
            form.save()
            return super().form_valid(form)
        else:
            return JsonResponse({"status": "error", "content": "You have no permissions"}, status=HTTPStatus.FORBIDDEN)


# Delete categories
class DeleteAdditionalServiceCategoryView(PermissionRequiredMixin, DeleteView):
    model = AdditionalServiceCategory
    permission_required = "manager.delete_additionalservicecategory"
    template_name = 'service_category_delete.html'
    success_url = reverse_lazy("service-category")

    def handle_no_permission(self):
        return JsonResponse({"status": "error", "content": "You have no permissions"}, status=HTTPStatus.FORBIDDEN)


# Add subcategories
class AdditionalServiceSubcategoryCreateView(CreateView):
    context = {}
    template_name = 'service_subcategory_form.html'
    form_class = AdditionalServiceSubcategoryForm

    def get_context_data(self, **kwargs):
        context = super(AdditionalServiceSubcategoryCreateView, self).get_context_data(**kwargs)
        context['subcategories'] = AdditionalServiceSubcategory.objects.all()
        return context

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        print(self.request.user.get_all_permissions())
        if self.request.user.has_perm('manager.add_additionalservicesubcategory'):
            form.save()
            return super().form_valid(form)
        else:
            return JsonResponse({"status": "error", "content": "You have no permissions"}, status=HTTPStatus.FORBIDDEN)


# Delete subcategories
class DeleteAdditionalServiceSubcategoryView(PermissionRequiredMixin, DeleteView):
    model = AdditionalServiceSubcategory
    permission_required = "manager.delete_additionalservicesubcategory"
    template_name = 'service_subcategory_delete.html'
    success_url = reverse_lazy("service-subcategory")

    def handle_no_permission(self):
        return JsonResponse({"status": "error", "content": "You have no permissions"}, status=HTTPStatus.FORBIDDEN)


class ServiceListView(LoginRequiredMixin, ListView):
    template_name = "service_list.html"
    context_object_name = "services"
    model = AdditionalService
    paginate_by = 10

    # ordering = "initial_date"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class ServiceCreateView(LoginRequiredMixin, CreateView):
    template_name = 'service_form.html'
    form_class = AdditionalServiceForm
    success_url = reverse_lazy("service-control-panel")

    def form_valid(self, form):
        if self.request.user.has_perm('manager.add.additionalservice'):
            form.save()
            return super().form_valid(form)
        else:
            return JsonResponse({"status": "error", "content": "You have no permissions"}, status=HTTPStatus.FORBIDDEN)


def load_subcategories(request, category_id):
    subcategories = AdditionalServiceSubcategory.objects.filter(belongs_to_id=category_id).order_by('name')
    return render(request, 'subcategory_dropdown_list_options.html', {'subcategories': subcategories})
