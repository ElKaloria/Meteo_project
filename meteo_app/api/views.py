from django.db.models import Count
from rest_framework.response import Response

from .serializers import *
from rest_framework.views import APIView
from meteo_app.models import UserHistory


class CityHistory(APIView):
    def get(self, request):
        queryset = UserHistory.objects.all().values('city').annotate(count=Count('city'))
        serializer = CityHistorySerializer(queryset, many=True)
        return Response(serializer.data)
    