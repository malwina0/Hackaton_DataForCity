from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Event
from .serializers import EventSerializer
import requests


# Create your views here.
@api_view(['GET'])
def get_current_events(request):
    r = requests.get(
        "https://api.um.warszawa.pl/api/action/events_calendar?id=fbf95b7b-ff95-48bc-afda-a16e968cc9a6&apikey=288c3c1c-0ad1-4d78-a934-b9b7abc96585")
    res = r.json()

    current_events = []
    for event in res["result"]:

        e, exists = Event.objects.get_or_create(**event)
        if not exists:
            e.save()

        current_events.append(e)

    serializer = EventSerializer(current_events, many=True)
    response = Response(serializer.data)
    response['Access-Control-Allow-Origin'] = '*'
    return response


@api_view(['GET'])
def get_event(reqeust, pk):
    event = Event.objects.get(pk=pk)
    serializer = EventSerializer(event)

    return Response(serializer.data)
