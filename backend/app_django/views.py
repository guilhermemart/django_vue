from rest_framework.views import APIView
from rest_framework.response import Response

from .models import alert, category
from .serializers import alert_serializer
from .main import update_alert_by_identificador

from .models import alert
from random import randint
from django.core.files.images import ImageFile
import os
from pathlib import Path


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
        DIR = Path(__file__).resolve().parent.parent.parent
        path = os.path.join("media", "uploads", "sauron_imagens", "n_avaliadas", "example.png")
        path = "media/uploads/sauron_imagens/n_avaliadas/example.png"
        absol_path = os.path.join(DIR, "media", "uploads", "sauron_imagens", "n_avaliadas", "example.png")
        fields = request.data
        categoria = category.objects.all()[0]
        with open(path, 'rb') as f:
            image = ImageFile(f)
            alerta_to_create = alert(
                alert_category=categoria,
                quantidade=fields.get("quantidade", randint(1, 3)),
                description=fields.get("description", ""),
                thumb_up=fields.get("thumb_up", False),
                thumb_down=fields.get("thumb_down", False),
                image=image,
                #image=ImageFile(open(fields.get("image_path", path))),
                local_image_url=fields.get("image_path", absol_path)
            )
            alerta_to_create.save()
            serializer = alert_serializer(alerta_to_create)
        return Response(serializer.data)
