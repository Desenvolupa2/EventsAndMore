from django.contrib.auth.views import LogoutView
from django.urls import path
from manager import views
from manager.views import *

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('events/<int:pk>', EventDetail.as_view(), name='event-detail'),
    path('stand-request/<int:pk>', ReserveStand.as_view(), name='stand-request'),
    path('stand-services/', ReserveAdditionalServices.as_view(), name='stand-services'),
    path('stand-request-grid/', StandRequestGrid.as_view(), name='stand-request-grid'),
    path('event-request/', EventRequestFormView.as_view(), name="event-request-form"),
    path('event-requests/', EventRequestListView.as_view(), name="event-request-list"),
    path('stand-reservations/', StandReservations.as_view(), name="stand-reservation-list"),
    path('event-requests/<int:pk>/', EventRequestUpdate.as_view(), name="event-request-update"),
    path('service-category/', AdditionalServiceCategoryCreateView.as_view(), name="service-category"),
    path('service-subcategory/', AdditionalServiceSubcategoryCreateView.as_view(), name="service-subcategory"),
    path('service-list/', ServiceListView.as_view(), name="service-list"),
    path('service-category/delete/<pk>', DeleteAdditionalServiceCategoryView.as_view(), name="delete-service-category"),
    path('service-subcategory/delete/<pk>', DeleteAdditionalServiceSubcategoryView.as_view(),
         name="delete-service-subcategory"),
    path('service-control-panel/', ServiceCreateView.as_view(), name="service-control-panel"),
    path('load-subcategories/<int:category_id>/', load_subcategories, name='load_subcategories'),
    path('load-services/<int:subcategory_id>/', load_additional_services, name='load_services'),
    path('event-layout/', EventLayout.as_view(), name='event-layout'),
    path('grid-positions/', GridPositions.as_view(), name='grid-positions'),
    path('grid-stands/', GridStands.as_view(), name='grid-stand'),
    path('catalog-control-panel/', CatalogCreateView.as_view(), name="catalog-control-panel"),
    path('delete-catalog/delete/<pk>', DeleteCatalog.as_view(), name="delete-catalog"),
    path('delete-service/delete/<pk>', DeleteService.as_view(), name="delete-service"),

]
