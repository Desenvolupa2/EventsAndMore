from django.urls import path

from manager.views import Home, EventRequestView

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('event-request', EventRequestView.as_view(), name="event-request"),
]
