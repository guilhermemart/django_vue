from django.http import Http404
from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import alert, category, red_zone, camera
from .serializers import alert_serializer, red_zone_serializer, camera_serializer, category_serializer
from .main import update_alert_by_identificador
from .watchdog_postgree import wait_for_new_alert

from random import randint
from django.core.files.images import ImageFile
import os
from pathlib import Path
from datetime import datetime
import pgpubsub


class latest_alerts_list(APIView):
    # devolve alertas sem filtro
    # usada para chamar a pagina dos alertas sem filtros
    def get(self, request, page):
        alertas = alert.objects.all()[6*(page-1):6*page]
        serializer = alert_serializer(alertas, many=True)
        return Response(serializer.data)


class alert_search(APIView):
    # devolve alertas filtrados de acordo com a data (timestamp)
    def get(self, request, init, end, page):
        alerts = alert.objects.filter(timestamp__gte=init)
        alerts = alerts.filter(timestamp__lte=end)[6*(page-1):6*page]
        serializer = alert_serializer(alerts, many=True)
        return Response(serializer.data)


class update_alert(APIView):
    def post(self, request):
        temp = request.data.get("identificador", "wrong_id")
        if temp == "wrong_id":
            print(temp)
        else:
            # a funcao update_alert_by_identificador usa os dados do request para alterar o alerta
            serializer = alert_serializer(update_alert_by_identificador(request), many=False)
            return Response(serializer.data)
        raise Http404


class create_alert(APIView):
    # cria um novo alerta de acordo com os dados do request
    def get(self, request):
        diretorio = Path().home()
        absol_path = os.path.join(diretorio, "media", "uploads", "sauron_imagens", "n_avaliadas", "example.png")
        path = absol_path
        fields = request.data
        categoria = category.objects.all()[0]
        categoria_input = category.objects.filter(name=fields.get('category_name','Nonconformity'))
        if categoria_input.count() > 0:
            categoria = categoria_input[0]
        alertas_qtde = alert.objects.all().count()
        with open(path, 'rb') as f:
            image = ImageFile(f)
            image.name = Path(image.name).name
            alerta_to_create = alert(
                alert_category=categoria,
                slug=fields.get("slug", f'example_{int(datetime.now().timestamp()*1000)}'),
                identificador=fields.get("identificador", int(datetime.now().timestamp()*1000)),
                quantidade=fields.get("quantidade", randint(1, 3)),
                anotacoes=fields.get("anotacoes", ""),
                thumb_up=fields.get("thumb_up", False),
                thumb_down=fields.get("thumb_down", False),
                image=image,
                local_image_url=fields.get("image_path", absol_path),
                sequencial=int(alertas_qtde+1)
            )
            alerta_to_create.save()
            try:
                pubsub = pgpubsub.connect(dbname="altave", user='altave', password='altave', host="localhost")
            except Exception as e:
                print(e)
            pubsub.notify('canal_1', 'mensagem_enviada')
            serializer = alert_serializer(alerta_to_create)
        return Response(serializer.data)


class alert_detail(APIView):
    # mostra uma pagina com o alerta e seus detalhes
    def get_object(self, category_slug, alert_slug):
        try:
            return alert.objects.filter(alert_category__slug=category_slug).filter(slug=alert_slug)[0]
        except alert.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, alert_slug, format=None):
        alerta = self.get_object(category_slug, alert_slug)
        serializer = alert_serializer(alerta)
        return Response(serializer.data)


class category_detail(APIView):
    # mostra uma pagina com o alerta e seus detalhes
    def get_object(self, category_slug):
        try:
            return category.objects.get(slug=category_slug)[0]
        except category.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        categoria = self.get_object(category_slug)
        serializer = category_serializer(categoria)
        return Response(serializer.data)


class load_red_zone(APIView):
    def get_red_zone(self, camera_slug, red_zone_slug):
        try:
            return red_zone.objects.filter(red_zone_camera__slug=camera_slug).filter(slug=red_zone_slug)[0]
        except red_zone.DoesNotExist:
            raise Http404

    def get_all_red_zones_dots(self, camera_slug):
        try:
            condensado = red_zone.objects.filter(red_zone_camera__slug=camera_slug)
            serializer = camera_serializer(condensado)
            all_red_zones = {}
            for red_zone_ in serializer.data:
                all_red_zones[red_zone_["name"]] = red_zone_['dots']
            return all_red_zones
        except camera.DoesNotExist:
            raise Http404

    def get(self, request, camera_slug, format=None):
        all_red_zone = self.get_all_red_zones_dots(camera_slug)
        return Response(all_red_zone)


class save_dots(APIView):
    def post(self, request, camera_slug):
        upload = request.files.get('txt')
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.txt', '.csv'):
            return f"File extension {ext} not allowed."
        save_path = os.path.join(os.getenv("HOME"), "Documents", "armazenamento", "sauron", f"{camera_slug}")
        upload.save(os.path.join(save_path, "temp"), overwrite=True)
        temp_upload = []
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        with open(os.path.join(save_path, "temp")) as up:
            for line in up:
                temp_upload.append(line.replace("\n", ""))
        file_path = os.path.join(save_path, f'{camera_slug}')
        up.close()
        with open(file_path, 'r') as arq:
            dt = []
            for line in arq:
                dt.append(line.replace("\n", ""))
            print(temp_upload)
            for el in temp_upload:
                dt.append(el)
        arq.close()
        with open(file_path, "w") as out:
            out.writelines("\n".join(dt))
        out.close()
        print(f"File {upload.filename} successfully saved to '{save_path}'.")
        return f"File {upload.filename} successfully saved to '{save_path}'."
        print(request.data.get("identificador"))
        serializer = alert_serializer(update_alert_by_identificador(request), many=False)
        return Response(serializer.data)


# o watchdog do front deve chamar essa função e deixar ela em watch
class wait_alert(APIView):
    def get(self, request):
        # o for abaixo fica travado esperando um novo alerta chegar
        for alert_ in wait_for_new_alert():
            serializer = alert_serializer(alert_, many=True)
            print("novo alerta recebido: " + datetime.now().isoformat())
            return Response(serializer.data)
