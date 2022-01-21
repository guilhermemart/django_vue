from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import alert, category
from .serializers import alert_serializer
from ..main import update_alert_by_id

class latest_alerts_list(APIView):
    def get(self, request, page):
        alertas = alert.objects.all()[6*(page-1):6*page]
        serializer = alert_serializer(alertas, many=True)
        return Response(serializer.data)


class update_alert(APIView):
    def get(self, request, _id):
        serializer = alert_serializer(update_alert_by_id(request), many=False)
        return Response(serializer.data)
