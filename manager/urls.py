from django.urls import path

from manager.views import (
    Home,
    EventRequestFormView,
    EventRequestListView,
    EventRequestStatusUpdate
)

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('event-request', EventRequestFormView.as_view(), name="event-request-form"),
    path('event-requests', EventRequestListView.as_view(), name="event-request-list"),
    path('event-request/<int:pk>/<int:status>', EventRequestStatusUpdate.as_view(), name="event-request-status"),
]
