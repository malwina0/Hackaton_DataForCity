from django.urls import path
from .views import get_current_predictions

urlpatterns = [
    path('get_smog/', get_current_predictions, name='get_current_predictions'),
]