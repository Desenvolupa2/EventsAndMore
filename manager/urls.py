from django.urls import path

from manager.views import (
    Home,
    Register,
    Login,
    EventRequestFormView,
    EventRequestListView,
    EventRequestStatusUpdate
)

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('event-request/', EventRequestFormView.as_view(), name="event-request-form"),
    path('event-requests/', EventRequestListView.as_view(), name="event-request-list"),
    path('event-request/<int:pk>/<int:status>', EventRequestStatusUpdate.as_view(), name="event-request-status"),
]
