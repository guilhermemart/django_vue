from django.http import Http404
from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import alert, category, red_zone, camera
from .serializers import alert_serializer, red_zone_serializer, camera_serializer, category_serializer
from .main import update_alert_by_identificador
from .wistml_sender import compose_witsml, send_witsml
from .watchdog_postgree import wait_for_new_alert
from .monthly_report_data import report_data

from random import randint
from django.core.files.images import ImageFile
import os
from pathlib import Path
from datetime import datetime, timedelta
import pgpubsub
from decouple import config
from dateutil.relativedelta import *



class latest_alerts_list(APIView):
    # devolve alertas sem filtro
    # usada para chamar a pagina dos alertas sem filtros
    def post(self, request, page):
        print(request.data)
        start = request.data["start"]
        end = request.data['end']
        thumb_up = request.data["valids"]  # mostrar thumb upeds
        thumb_down = request.data['invalids']  # mostrar thumbdown eds
        non_classified = request.data['non_classifieds']  # mostrar não classificados
        # filtragem por data
        alerts = alert.objects.filter(timestamp__gte=start + 1)
        alerts = alerts.filter(timestamp__lte=end + 1)
        # filtragem por classificacao
        alerts = alerts.filter(thumb_up__exact=not thumb_up)
        alerts = alerts.filter(thumb_down__exact=not thumb_down)
        alerts = alerts.filter(thumb_down__exact=not non_classified)[6 * (page - 1):(6 * page) + 1]
        # 6 o numero magico de alertas na pagina
        # retorna 7 valores o 7th serve para o vue definir se tem proxima pagina
        serializer = alert_serializer(alerts, many=True)
        print(serializer.data)
        return Response(serializer.data)
        # Response transforma o serializer em um objeto javascript pro vue

class alert_search(APIView):
    # devolve alertas filtrados de acordo com a data (timestamp)
    def get(self, request, init, end, page):
        alerts = alert.objects.filter(timestamp__gte=init)
        alerts = alerts.filter(timestamp__lte=end)[6 * (page - 1):(6 * page) + 1]
        serializer = alert_serializer(alerts, many=True)
        return Response(serializer.data)


class update_alert(APIView):
    def post(self, request):
        temp = request.data.get("identificador", "wrong_id")
        if temp == "wrong_id":
            print(temp)
        else:
            # a funcao update_alert_by_identificador usa os dados do request para alterar o alerta
            serializer = alert_serializer(update_alert_by_identificador(request))
            if str(serializer.data.thumb_up).lower() == "true":
                try:
                    send_witsml(config("WITSML_USER"), config("WITSML_PASS"), config("WITSML_URL"), serializer)
                except Exception as e:
                    print(f"impossivel criar xml {e}")
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
        categoria_input = category.objects.filter(name=fields.get('category_name', 'Nonconformity'))
        if categoria_input.count() > 0:
            categoria = categoria_input[0]
        alertas_qtde = alert.objects.all().count()
        with open(path, 'rb') as f:
            image = ImageFile(f)
            image.name = Path(image.name).name
            alerta_to_create = alert(
                alert_category=categoria,
                slug=fields.get("slug", f'example_{int(datetime.now().timestamp() * 1000)}'),
                identificador=fields.get("identificador", int(datetime.now().timestamp() * 1000)),
                date_added=datetime.now().replace(month=12),
                quantidade=fields.get("quantidade", randint(1, 3)),
                anotacoes=fields.get("anotacoes", ""),
                thumb_up=fields.get("thumb_up", False),
                thumb_down=fields.get("thumb_down", True),
                image=image,
                local_image_url=fields.get("image_path", absol_path),
                sequencial=int(alertas_qtde + 1),
                witsml_confirm="witsml_not_sent"
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


class load_red_zones(APIView):
    def get(self, request, cam):
        red_zones = red_zone.objects.filter(red_zone_camera__name=f"cam{cam}")
        serializer = red_zone_serializer(red_zones, many=True)
        return Response(serializer.data)
        # o serializer.data possui bem mais campos que os utilizados no front
        # nao atrapalha ter mais campos
        # name, height, width, enabled e dots são obrigatorios


# deve receber os dados basicos de uma redzone e criar o txt, conteudo
class save_red_zone(APIView):
    def post(self, request):
        print(request.data)
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
        serializer = alert_serializer(update_alert_by_identificador(request))
        return Response(serializer.data)


# o watchdog do front deve chamar essa função e deixar ela em watch
class wait_alert(APIView):
    def get(self, request):
        # o for abaixo fica travado esperando um novo alerta chegar
        for alert_ in wait_for_new_alert():
            serializer = alert_serializer(alert_, many=True)
            print("novo alerta recebido: " + datetime.now().isoformat())
            return Response(serializer.data)


# Monthly Report - Dados mensais (dia atual, esse mês e mês passado)
class alerts_report(APIView):
    def get(self, request):
        # Cria as datas, e coloca a 'time_past' como sendo -1 mês.
        # Essa lib 'relativedelta' faz com que pegue sempre uma data do mês anterior,
        # mesmo se for dia 31 de março irá cair no dia 28 de fevereiro
        time_now = datetime.now()
        time_past = time_now + relativedelta(months=-1)
        # Utiliza as timestamps do início do mês passado, desse mês e hoje, para filtrar os resultados do banco
        # Multiplica por 1000 porque nesse timestamp o milisegundo é separado por virgula, exemplo:
        # stamp_past_start = 1643684400.0
        # timestamp alerta = 1612143950000
        # Ou seja, é mil vezes menor que a timestamp do alerta que não tem ponto, é tudo junto
        stamp_past_start = time_past.replace(day=1, hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000
        stamp_now_start = time_now.replace(day=1, hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000
        stamp_today = time_now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000
        #TIMEZONE - SE PEGA SEM TIMEZONE OU CONSIDERA A DO BRASIL
        alerts = alert.objects.filter(timestamp__gte=stamp_past_start)
        alerts_past = alerts.filter(timestamp__lt=stamp_now_start)
        alerts_now = alerts.filter(timestamp__gte=stamp_now_start)
        alerts_today = alerts.filter(timestamp__gte=stamp_today)
        serializer_past = alert_serializer(alerts_past, many=True).data
        serializer_now = alert_serializer(alerts_now, many=True).data
        serializer_today = alert_serializer(alerts_today, many=True).data
        months = {"01": "January / ", "02": "February / ", "03": "March / ",
                  "04": "April / ", "05": "May / ", "06": "June / ",
                  "07": "July / ", "08": "August / ", "09": "September / ",
                  "10": "October / ", "11": "November / ", "12": "December / "}
        now_month = months[str(time_now)[5:7]] + str(time_now)[:4]
        past_month = months[str(time_past)[5:7]] + str(time_past)[:4]
        # Usa a função 'report_data' para criar os dicionários. Ver o arquivo 'monthly_report_data.py'
        data_past = report_data(serializer_past)
        data_past["month"] = past_month
        data_now = report_data(serializer_now)
        data_now["month"] = now_month
        data_today = report_data(serializer_today)
        data_today["month"] = "Today"
        # Salva os 3 dicts em um único dict e envia para o front
        result = {"today": data_today, "now": data_now, "past": data_past}
        return Response(result)
