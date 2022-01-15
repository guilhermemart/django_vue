from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import alert
from .serializers import alert_serializer


class latest_alerts_list(APIView):
    def get(self, request, page):
        alertas = alert.objects.all()[6*(page-1):6*page]
        serializer = alert_serializer(alertas, many=True)
        return Response(serializer.data)