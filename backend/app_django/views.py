from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import alert, category, red_zone, camera, condensed_red_zones
from .serializers import alert_serializer, red_zone_serializer, all_red_zone_serializer
from .main import update_alert_by_identificador

from random import randint
from django.core.files.images import ImageFile
import os
from pathlib import Path
from datetime import datetime


class latest_alerts_list(APIView):
    def get(self, request, page):
        alertas = alert.objects.all()[6*(page-1):6*page]
        serializer = alert_serializer(alertas, many=True)
        return Response(serializer.data)


class update_alert(APIView):
    def post(self, request):
        print(request.data.get("identificador"))
        serializer = alert_serializer(update_alert_by_identificador(request), many=False)
        return Response(serializer.data)


class create_alert(APIView):
    def get(self, request):
        DIR = Path().home()
        absol_path = os.path.join(DIR, "media", "uploads", "sauron_imagens", "n_avaliadas", "example.png")
        path = absol_path
        fields = request.data
        categoria = category.objects.all()[0]
        with open(path, 'rb') as f:
            image = ImageFile(f)
            image.name = Path(image.name).name
            alerta_to_create = alert(
                alert_category=categoria,
                identificador=fields.get("identificador", int(datetime.now().timestamp()*1000)),
                quantidade=fields.get("quantidade", randint(1, 3)),
                description=fields.get("description", ""),
                thumb_up=fields.get("thumb_up", False),
                thumb_down=fields.get("thumb_down", False),
                image=image,
                local_image_url=fields.get("image_path", absol_path)
            )
            alerta_to_create.save()
            serializer = alert_serializer(alerta_to_create)
        return Response(serializer.data)


class alert_detail(APIView):
    def get_object(self, category_slug, alert_slug):
        try:
            return alert.objects.filter(alert_category__slug=category_slug).get(slug=alert_slug)
        except alert.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        alerta = self.get_object(category_slug, product_slug)
        serializer = alert_serializer(alerta)
        return Response(serializer.data)

class load_red_zone(APIView):
    def get_red_zone(self, camera_slug, red_zone_slug):
        try:
            return red_zone.objects.filter(red_zone_camera__slug=camera_slug).get(slug=red_zone_slug)
        except red_zone.DoesNotExist:
            raise Http404

    def get_all_red_zones(self, camera_slug):
        try:
            condensado = condensed_red_zones.objects.filter(red_zone_camera__slug=camera_slug)[0]
            return condensado
        except condensed_red_zones.DoesNotExist:
            raise Http404

    def get(self, request, camera_slug, format=None):
        all_red_zone = self.get_all_red_zones(camera_slug)
        serializer = all_red_zone_serializer(all_red_zone)
        return Response(serializer.data)
