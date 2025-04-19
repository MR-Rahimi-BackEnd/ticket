from django.urls import path ,include
from . import views
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


router = routers.DefaultRouter()
router.register('envent' , views.EventViewSet , basename='event')
router.register('ticket' , views.TicketViewSet , basename='ticket')
router.register('attendee' , views.AttendeeViewSet , basename='attendee')

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path('api/',include(router.urls)),
]


