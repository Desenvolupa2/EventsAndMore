from django.urls import path

from manager.views import (
    Home,
    Register,
    Login,
)

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
]
