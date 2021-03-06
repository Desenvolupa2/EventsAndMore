import io
import json
import uuid
from http import HTTPStatus
from typing import List

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.files import File
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import context
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, TemplateView
from reportlab.pdfgen import canvas
from django.conf import settings

from manager.filters import EventRequestsFilter
from manager.forms import (AdditionalServiceCategoryForm, AdditionalServiceForm, AdditionalServiceSubcategoryForm,
                           CatalogForm, EventRequestForm, NewUserForm, StandForm)
from manager.models import (AdditionalService, AdditionalServiceCategory, AdditionalServiceReservation,
                            AdditionalServiceSubcategory, Catalog, Event,
                            EventContract, EventInvoice, EventRequest, EventRequestStand, EventRequestStatus,
                            GridPosition, Reservation, ReservationContract, ReservationStatus, Stand, StandReservation)


class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        events = Event.objects.all().filter(initial_date__gte=timezone.now()).order_by("initial_date")
        images = ["images/green.jpg", "images/rose.jpg", "images/blue.jpg"]
        context["next_events"] = [(image, event) for image, event in zip(images, events[:3])]
        context["events"] = events
        return context


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
        description = body.get('description')
        initial_date = parse_date(body.get('initialDate'))
        final_date = parse_date(body.get('finalDate'))
        grid = body.get('grid')
        if not event_name:
            return JsonResponse({"status": "error", "content": "Invalid event name"}, status=HTTPStatus.BAD_REQUEST)

        if not description:
            return JsonResponse({"status": "error", "content": "Invalid description"}, status=HTTPStatus.BAD_REQUEST)

        if not initial_date or not final_date:
            return JsonResponse({"status": "error", "content": "Invalid dates"}, status=HTTPStatus.BAD_REQUEST)

        if not grid:
            return JsonResponse({"status": "error", "content": "Invalid grid selection"}, status=HTTPStatus.BAD_REQUEST)

        event_request = EventRequest(
            name=event_name,
            description=description,
            initial_date=initial_date,
            final_date=final_date,
            entity=self.request.user,
            status=EventRequestStatus.PENDING_ON_MANAGER
        )

        stands_requested = set()

        grid_positions = [GridPosition.objects.get(x_position=row, y_position=col) for row, col in grid]
        event_stand_requests = []
        for grid_position in grid_positions:
            stand_positions = GridPosition.objects.filter(stand=grid_position.stand)
            if any(position not in grid_positions for position in stand_positions):
                return JsonResponse(
                    {"status": "error", "content": "A stand must be selected in its entirety"},
                    status=HTTPStatus.BAD_REQUEST
                )

            if grid_position.stand not in stands_requested:
                stands_requested.add(grid_position.stand)
                event_stand_requests.append(EventRequestStand(event_request=event_request, stand=grid_position.stand))

        event_request.save()
        for event_stand_request in event_stand_requests:
            event_stand_request.save()

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
        if body.get("status") == EventRequestStatus.ACCEPTED:
            event = Event.objects.create(
                name=event_request.name,
                description=event_request.description,
                initial_date=event_request.initial_date,
                final_date=event_request.final_date,
            )
            EventInvoice.objects.create(
                event_request=event_request,
                event=event
            )

            pdf_buffer = self._generate_pdf_contract(event_request)
            contract_uuid = uuid.uuid4()
            EventContract.objects.create(
                uuid=contract_uuid,
                event_request=event_request,
                event=event,
                file=File(pdf_buffer, name=f"{contract_uuid}.pdf")
            )
        return JsonResponse({"status": "success", "content": model_to_dict(event_request)}, status=HTTPStatus.OK)

    def _generate_pdf_contract(self, event_request: 'EventRequest') -> io.BytesIO:
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(50, 800, "EVENTS AND MORE")
        p.drawString(200, 700, "EVENT RESERVATION CONTRACT")

        p.drawString(100, 600, "Event reservation name: " + str(event_request.name))
        p.drawString(100, 580, "Initial date: " + str(event_request.initial_date))
        p.drawString(100, 560, "Final date: " + str(event_request.final_date))
        p.drawString(100, 540, "Having the contract been signed, the reservation is confirmed.")

        p.drawString(100, 500, "Reservation made by: " + str(self.request.user))
        p.drawString(100, 480, "Entity contact email address: " + str(self.request.user.email))

        p.drawString(100, 440, "The payment is to be made by bank transfer. If the payment is not done in 7 ")
        p.drawString(100, 420, "days the reservation will be canceled.")

        p.drawString(100, 380, "If need of cancellation, the client must contact the event organizer.")

        p.drawString(100, 340, "The parties agree to follow the cityhall, catalan and spanish laws.")

        p.drawImage(settings.MEDIA_ROOT / "logo-eventsandmore.png", 70, 100, 150, 150)
        p.drawString(470, 50, "Page 1 of 1.")
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer


# Create catalogs
class CatalogCreateView(CreateView):
    context = {}
    template_name = 'catalog_form.html'
    form_class = CatalogForm

    def get_context_data(self, **kwargs):
        context = super(CatalogCreateView, self).get_context_data(**kwargs)
        context['catalogs'] = Catalog.objects.all()
        return context

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        if self.request.user.has_perm('manager.add_catalog'):
            form.save()
            return super().form_valid(form)
        else:
            return JsonResponse({"status": "error", "content": "You have no permissions"}, status=HTTPStatus.FORBIDDEN)


# Delete catalogs
class DeleteCatalog(PermissionRequiredMixin, DeleteView):
    model = Catalog
    permission_required = "manager.delete_catalog"
    template_name = 'catalog_delete.html'
    success_url = reverse_lazy("catalog-control-panel")

    def handle_no_permission(self):
        return JsonResponse({"status": "error", "content": "You have no permissions"}, status=HTTPStatus.FORBIDDEN)


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
    success_url = reverse_lazy("service-list")

    def form_valid(self, form):
        if self.request.user.has_perm('manager.add_additionalservice'):
            form.save()
            return super().form_valid(form)
        else:
            return JsonResponse({"status": "error", "content": "You have no permissions"}, status=HTTPStatus.FORBIDDEN)


# Delete services
class DeleteService(PermissionRequiredMixin, DeleteView):
    model = AdditionalService
    permission_required = "manager.delete_service"
    template_name = 'service_delete.html'
    success_url = reverse_lazy("service-list")

    def handle_no_permission(self):
        return JsonResponse({"status": "error", "content": "You have no permissions"}, status=HTTPStatus.FORBIDDEN)


def load_categories(request):
    categories = AdditionalServiceCategory.objects.all().order_by('name')
    return JsonResponse({"categories": [model_to_dict(category) for category in categories]})


def load_subcategories(request, category_id):
    subcategories = AdditionalServiceSubcategory.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'subcategory_dropdown_list_options.html', {'subcategories': subcategories})


def load_additional_services(request, subcategory_id):
    services = AdditionalService.objects.filter(subcategory_id=subcategory_id).order_by('name')
    return render(request, 'service_dropdown_list_options.html', {'services': services})


class EventLayout(PermissionRequiredMixin, TemplateView):
    template_name = "event_layout.html"
    permission_required = "can_define_layout"


class GridPositions(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        initial_date = parse_date(self.request.GET.get('initial_date'))
        final_date = parse_date(self.request.GET.get('final_date'))
        if not initial_date or not final_date:
            return JsonResponse({"status": "error", "content": "Invalid format"}, status=HTTPStatus.BAD_REQUEST)

        stands_same_date = [
            stand_request.stand for stand_request in EventRequestStand.objects.filter(
                event_request__in=EventRequest.objects.filter(
                    status=EventRequestStatus.ACCEPTED
                ).exclude(
                    final_date__lt=initial_date,
                ).exclude(
                    initial_date__gt=final_date
                ),
            )
        ]

        positions = {}
        for grid_position in GridPosition.objects.all():
            if grid_position.stand is not None:
                if grid_position.stand.id not in positions.keys():
                    positions[grid_position.stand.id] = []
                positions[grid_position.stand.id].append(
                    {**model_to_dict(grid_position, exclude=['id', 'stand', 'creation_date', 'update_date']),
                     **{"available": grid_position.stand not in stands_same_date}})

        return JsonResponse({"status": "success", "content": positions}, status=HTTPStatus.OK)


class GridStands(LoginRequiredMixin, View):

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
        if not self.request.user.has_perm("change_grid_position"):
            return JsonResponse({"status": "error", "content": "No permissions"}, status=HTTPStatus.FORBIDDEN)
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


class ReserveStand(LoginRequiredMixin, FormView):
    template_name = "stand_form.html"
    form_class = StandForm

    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(self.request.body)
        except:
            return JsonResponse({"status": "error", "content": "Unexpected format"}, status=HTTPStatus.BAD_REQUEST)
        event_id = kwargs.get('pk')
        stands = body.get('grid')
        whole_event = body.get('wholeEvent')

        if not stands:
            return JsonResponse({"status": "error", "content": "Invalid selection"}, status=HTTPStatus.BAD_REQUEST)

        if not event_id:
            return JsonResponse({"status": "error", "content": "Invalid event"}, status=HTTPStatus.BAD_REQUEST)

        event = Event.objects.get(pk=event_id)

        initial_date = None
        final_date = None
        if not whole_event:
            initial_date = parse_date(body.get('initial_date'))
            final_date = parse_date(body.get('final_date'))

            if not initial_date or not final_date:
                return JsonResponse({"status": "error", "content": "Invalid dates"}, status=HTTPStatus.BAD_REQUEST)

            if initial_date < event.initial_date or final_date > event.final_date:
                return JsonResponse(
                    {"status": "error", "content": "Dates are outside the duration of the event"},
                    status=HTTPStatus.BAD_REQUEST
                )

        stands_to_reserve = []
        for grid_stand in stands.values():
            positions = [GridPosition.objects.get(x_position=x, y_position=y) for x, y in grid_stand]
            expected_positions = GridPosition.objects.filter(stand__in=[p.stand for p in positions])
            if len(set(expected_positions) - set(positions)) != 0:
                return JsonResponse(
                    {"status": "error", "content": "Can't select half stand"},
                    status=HTTPStatus.UNPROCESSABLE_ENTITY
                )
            stands_to_reserve.append(positions[0].stand)

        reservation = Reservation.objects.create(
            event=event,
            initial_date=initial_date or event.initial_date,
            final_date=final_date or event.final_date,
            status=ReservationStatus.PENDING
        )

        stand_reservations = [
            StandReservation.objects.create(reservation=reservation, stand=stand)
            for stand in stands_to_reserve
        ]
        pdf_buffer = self._generate_pdf_contract(reservation, stand_reservations)
        contract_uuid = uuid.uuid4()
        ReservationContract.objects.create(
            uuid=contract_uuid,
            client=self.request.user,
            booking=reservation,
            file=File(pdf_buffer, name=f"{contract_uuid}.pdf")
        )

        return JsonResponse({"status": "success", "content": {"reservation": reservation.id}})

    def _generate_pdf_contract(
            self,
            reservation: 'Reservation',
            stand_reservations: List['StandReservation']
    ) -> io.BytesIO:
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(50, 800, "EVENTS AND MORE")
        p.drawString(200, 700, "STAND RESERVATION CONTRACT")

        p.drawString(100, 600, "Stand reservation of the following event: " + str(reservation.event))
        p.drawString(100, 580, "Initial date: " + str(reservation.initial_date))
        p.drawString(100, 560, "Final date: " + str(reservation.final_date))
        p.drawString(100, 540, "Having the contract been signed, the reservation is confirmed.")

        p.drawString(100, 500, "Reservation made by: " + str(self.request.user))
        p.drawString(100, 480, "Entity contact email address: " + str(self.request.user.email))

        p.drawString(100, 440, "The payment is to be made by bank transfer. If the payment is not done in 7 ")
        p.drawString(100, 420, "days the reservation will be canceled.")

        p.drawString(100, 380, "If need of cancellation, the client must contact the event organizer.")

        p.drawString(100, 340, "The parties agree to follow the cityhall, catalan and spanish laws.")

        p.drawImage(settings.MEDIA_ROOT / "logo-eventsandmore.png", 70, 100, 150, 150)
        p.drawString(470, 50, "Page 1 of 1.")
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer


class ReserveAdditionalServices(LoginRequiredMixin, TemplateView):
    template_name = "stand_services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservation_id = self.request.GET.get('reservation')
        context['reservation'] = Reservation.objects.get(pk=reservation_id)
        context['stand_reservations'] = StandReservation.objects.filter(reservation_id=reservation_id)
        context['categories'] = AdditionalServiceCategory.objects.all()
        return context

    def post(self, *args, **kwargs):
        try:
            body = json.loads(self.request.body)
        except:
            return JsonResponse({"status": "error", "content": "Unexpected format"}, status=HTTPStatus.BAD_REQUEST)

        reservation_id = body.get("reservation")
        stand_reservations_services = body.get("services")
        if not reservation_id or stand_reservations_services is None:
            return JsonResponse({"status": "error", "content": "Unexpected values"}, status=HTTPStatus.BAD_REQUEST)

        reservation = Reservation.objects.get(pk=reservation_id)

        for stand_reservation in stand_reservations_services:
            for service_id, quantity, comments in stand_reservations_services[stand_reservation]:
                AdditionalServiceReservation.objects.create(
                    stand_reservation_id=stand_reservation,
                    additional_service_id=service_id,
                    quantity=quantity,
                    comments=comments,
                    initial_date=reservation.initial_date,
                    final_date=reservation.final_date,
                )
        reservation.status = ReservationStatus.CONFIRMED
        reservation.save()
        return JsonResponse({"status": "success", "content": "Additional services submitted"}, status=HTTPStatus.OK)


class EventDetail(DetailView):
    model = Event
    context_object_name = "event"
    template_name = "event_detail.html"


class StandRequestGrid(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        event_id = self.request.GET.get('event')
        if not event_id:
            return JsonResponse("Invalid event", status=HTTPStatus.BAD_REQUEST)

        event_request = EventRequest.objects.get(eventcontract=EventContract.objects.get(event_id=event_id))
        stands = [e.stand for e in EventRequestStand.objects.filter(event_request=event_request)]
        out = []
        for stand in stands:
            positions = [[gp.x_position, gp.y_position] for gp in GridPosition.objects.filter(stand=stand)]
            is_available = StandReservation.objects.filter(
                stand=stand,
                reservation__in=Reservation.objects.filter(event_id=event_id, status=ReservationStatus.CONFIRMED)
                # TODO: also filter by date
            ).count() == 0
            out.append({"available": is_available, "positions": positions})
        return JsonResponse({"status": "success", "content": out}, status=HTTPStatus.OK)


class StandReservations(LoginRequiredMixin, TemplateView):
    template_name = "stand_reservations.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        user_reservations = Reservation.objects.filter(
            reservationcontract__in=ReservationContract.objects.filter(client=self.request.user)
        )
        d = {}
        for user_reservation in user_reservations:
            d[user_reservation] = list(StandReservation.objects.filter(reservation=user_reservation))
        context['stand_reservations'] = d
        return context


class AboutUs(TemplateView):
    template_name = "about_us.html"
