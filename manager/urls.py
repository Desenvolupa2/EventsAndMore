from django.contrib.auth.views import LogoutView
from django.urls import path

from manager.views import (
    Home,
    Register,
    Login,
    EventRequestFormView,
    EventRequestListView,
    EventRequestUpdate
)

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('event-request/', EventRequestFormView.as_view(), name="event-request-form"),
    path('event-requests/', EventRequestListView.as_view(), name="event-request-list"),
    path('event-requests/<int:pk>/', EventRequestUpdate.as_view(), name="event-request-update"),
    path('service-category/', AdditionalServiceCategoryCreateView.as_view(), name="service"),
    path('service-subcategory/', AdditionalServiceSubcategoryCreateView.as_view(), name="service-subcategory"),
    # path('add-service/', AdditionalServiceFormView.as_view(), name="add-service"),
    path('service-list/', EventRequestListView.as_view(), name="event-request-list"),
    path('service-category/delete/<pk>', DeleteAdditionalServiceCategoryView.as_view(), name="delete-service-category"),
    path('service-subcategory/delete/<pk>', DeleteAdditionalServiceSubcategoryView.as_view(),
         name="delete-service-subcategory"),

]
