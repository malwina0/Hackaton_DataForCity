from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from rest_framework.response import Response
from .serializers import SmogSerializer
from .models import SmogPrediction


# Create your views here.

@api_view(['GET'])
def get_current_predictions(request):
    today_date = datetime.today()
    current_dates = [today_date + timedelta(days=1), today_date + timedelta(days=2), today_date + timedelta(days=3)]

    # ADD CODE TO AUTOMATE PREDICTIONS

    smog_predictions = SmogPrediction.objects.filter(date__in=current_dates)
    serializer = SmogSerializer(smog_predictions, many=True)
    response = Response(serializer.data)
    response['Access-Control-Allow-Origin'] = '*'
    return response