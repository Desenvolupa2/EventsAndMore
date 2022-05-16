import json
from http import HTTPStatus
from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.views import View
from django.views.generic import CreateView, DeleteView, FormView, ListView, TemplateView

from manager.filters import EventRequestsFilter
from manager.forms import (
    AdditionalServiceCategoryForm,
    AdditionalServiceForm,
    AdditionalServiceSubcategoryForm,
    EventRequestForm,
    NewUserForm
)

from manager.models import (
    AdditionalService,
    AdditionalServiceCategory,
    AdditionalServiceSubcategory,
    EventRequest,
    EventRequestStand,
    EventRequestStatus,
    GridPosition,
    Stand
)


class Home(TemplateView):
    template_name = "home.html"


class Register(CreateView):
    form_class = NewUserForm
    template_name = "register.html"
    success_url = reverse_lazy("login")


class Login(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")


class EventRequestFormView(LoginRequiredMixin, FormView):
    template_name = "event_request_form.html"
    form_class = EventRequestForm
    success_url = reverse_lazy("event-request-list")

    def post(self, request, *args, **kwargs):
        body = json.loads(self.request.body)
        event_name = body.get('eventName')
        initial_date = parse_date(body.get('initialDate'))
        final_date = parse_date(body.get('finalDate'))
        grid = body.get('grid')
        if not event_name or not initial_date or not final_date or not grid:
            return JsonResponse({"status": "error", "content": "Invalid format"}, status=HTTPStatus.BAD_REQUEST)

        event_request = EventRequest.objects.create(
            name=event_name,
            initial_date=initial_date,
            final_date=final_date,
            entity=self.request.user,
            status=EventRequestStatus.PENDING_ON_MANAGER
        )
        event_request.save()

        stands_requested = set()

        for row, col in grid:
            grid_position = GridPosition.objects.get(x_position=row, y_position=col)
            if grid_position.stand not in stands_requested:
                stands_requested.add(grid_position.stand)
                event_request_stand = EventRequestStand(event_request=event_request, stand=grid_position.stand)
                event_request_stand.save()

        return HttpResponse(status=HTTPStatus.OK)


class EventRequestListView(LoginRequiredMixin, TemplateView):
    template_name = "event_request_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        queryset = EventRequest.objects.all()
        if not self.request.user.has_perm("change_event_request"):
            queryset = queryset.filter(entity=self.request.user)
        queryset = queryset.order_by("status", "-initial_date")
        context["filter"] = EventRequestsFilter(self.request.GET, queryset=queryset)
        return context


class EventRequestUpdate(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)

    def put(self, *args, **kwargs):
        pk = kwargs.get('pk')
        event_request = EventRequest.objects.get(id=pk)

        if not self.request.user.has_perm("change_event_request") and (
            event_request.status is not EventRequestStatus.PENDING_ON_ORGANIZER
            and event_request.entity is not self.request.user
        ):
            return JsonResponse(
                {"status": "error", "content": "You have no permissions. This request can't be updated"},
                status=HTTPStatus.FORBIDDEN,
            )

        if event_request is None:
            return JsonResponse({"status": "error", "content": "Invalid pk"}, status=HTTPStatus.BAD_REQUEST)

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
    subcategories = AdditionalServiceSubcategory.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'subcategory_dropdown_list_options.html', {'subcategories': subcategories})


class EventLayout(TemplateView):
    template_name = "event_layout.html"


class GridPositions(View):

    def get(self, request, *args, **kwargs):
        initial_date = parse_date(self.request.GET.get('initial_date'))
        final_date = parse_date(self.request.GET.get('final_date'))
        if not initial_date or not final_date:
            return JsonResponse({"status": "error", "content": "Invalid format"}, status=HTTPStatus.BAD_REQUEST)

        stands_same_date = [
            stand_request.stand for stand_request in EventRequestStand.objects.filter(
                event_request__in=EventRequest.objects.filter(
                    initial_date__gte=initial_date,
                    final_date__lte=final_date,
                    status=EventRequestStatus.ACCEPTED)
            )
        ]

        occupied_positions = list(chain.from_iterable([
            GridPosition.objects.filter(stand=stand)
            for stand in stands_same_date
        ]))

        positions = {}
        for grid_position in GridPosition.objects.all():
            if grid_position.stand is not None:
                if grid_position.stand.id not in positions.keys():
                    positions[grid_position.stand.id] = []
                positions[grid_position.stand.id].append(
                    {**model_to_dict(grid_position, exclude=['id', 'stand', 'creation_date', 'update_date']),
                     **{"available": grid_position not in occupied_positions}})

        return JsonResponse({"status": "success", "content": positions}, status=HTTPStatus.OK)


class GridStands(View):

    def get(self, request, *args, **kwargs):
        content = {}

        for position in GridPosition.objects.all():
            if position.stand is None:
                if 'unassigned' not in content.keys():
                    content['unassigned'] = []
                content['unassigned'].append([position.x_position, position.y_position])
            else:
                if position.stand.id not in content.keys():
                    content[position.stand.id] = []
                content[position.stand.id].append([position.x_position, position.y_position])

        return JsonResponse({"status": "success", "content": content}, status=HTTPStatus.OK)

    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(self.request.body)
        except:
            return JsonResponse({"status": "error", "content": "Unexpected format"}, status=HTTPStatus.BAD_REQUEST)

        positions = body.get('positions')
        if positions is None:
            return JsonResponse({"status": "error", "content": "Unexpected format"}, status=HTTPStatus.BAD_REQUEST)
        stand = Stand()
        stand.save()
        new_grid_positions = []
        for x, y in positions:
            grid_position = GridPosition.objects.get(x_position=x, y_position=y)
            if grid_position.stand is None:
                grid_position.stand = stand
                new_grid_positions.append(grid_position)
            else:
                return JsonResponse(
                    {"status": "error", "content": "This position is already assigned"},
                    status=HTTPStatus.BAD_REQUEST
                )

        for grid_position in new_grid_positions:
            grid_position.save()
        return JsonResponse(
            {"status": "success", "content": f"Positions {positions} created successfully"},
            status=HTTPStatus.OK
        )
