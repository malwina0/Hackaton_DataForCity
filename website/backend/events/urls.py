from django.urls import path
from .views import get_current_events, get_event

urlpatterns = [
    path('get_events/', get_current_events, name='get_events'),
    path('get_events/<str:pk>/', get_event, name='get_event'),
]