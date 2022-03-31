from django.urls import path

from manager.views import Home

urlpatterns = [
    path('', Home.as_view(), name="home")
]