from rest_framework.serializers import ModelSerializer
from .models import SmogPrediction


class SmogSerializer(ModelSerializer):
    class Meta:
        model = SmogPrediction
        fields = '__all__'