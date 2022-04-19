from django.urls import path

from manager.views import (
    Home,
    register_user,
    Login,
)

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('register', register_user, name='register'),
    path('login', Login.as_view(), name='login'),
]
