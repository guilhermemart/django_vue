

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import alert, category, red_zone, camera
from .serializers import alert_serializer, red_zone_serializer, camera_serializer, category_serializer
from .main import update_alert_by_identificador
from .wistml_sender import compose_witsml, send_witsml
from .watchdog_postgree import wait_for_new_alert

from random import randint
from django.core.files.images import ImageFile
from django.core.files import File
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone
import pgpubsub
from decouple import config
from dateutil.relativedelta import *


# pip install python-dateutil


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
        path = Path().home().joinpath("media", "uploads", "sauron_imagens", "n_avaliadas", "example.png")

        fields = request.data
        categoria = category.objects.all()[0]
        categoria_input = category.objects.filter(name=fields.get('category_name', 'Nonconformity'))
        if categoria_input.count() > 0:
            categoria = categoria_input[0]
        alertas_qtde = alert.objects.all().count()
        with path.open(mode='rb') as f:
            image = ImageFile(f)
            image.name = path.name
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
                local_image_url=fields.get("image_path", str(path)),
                sequencial=int(alertas_qtde + 1),
                witsml_confirm="witsml_not_sent"
            )
            alerta_to_create.save()
            try:
                pubsub = pgpubsub.connect(dbname=config('db'), user=config('user'), password=config('password'), host=config('db_host'))
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
        output = request.data
        output_string = f"nome: {output['name']}, largura: {output['width']}, pontos: "
        for ponto in output["dots"]:
            output_string = output_string + ponto + ","
        # caminho dos arquivos no settings django
        save_path = os.path.join(os.getenv("HOME"), "media", "uploads", "red_zones", "individual_red_zones", f"{output['name']}.txt")
        # precisa da lib Pathlib para salvar o arquivo
        path = Path().home().joinpath('media','uploads','red_zones','individual_red_zones',f'{output["name"]}.txt')
        with open(save_path, 'w') as rzone:
            rzone.write(output_string)
            rzone.close()
        camera_number=request.output['cam'][0]
        wich_camera = camera.objects.filter(name="cam"+str(camera_number))
        date_added=datetime.now(tz=timezone(timedelta(hours=-3)))
        ident=date_added.timestamp()
        r_zone_file_path= path  # r_zone_file_path = save_path nao aceitou o metodo File()
        with r_zone_file_path.open(mode="rb") as f:
            new_red_zone = red_zone(
                identificador=str(ident),
                red_zone_camera=wich_camera,
                slug=f"red_zone_cam{camera_number}_{ident}",
                timestamp=1000*ident,
                date_added=date_added,
                name=f"red_zone_cam{camera_number}_{ident}",
                dots=output['dots'],
                enabled=True,
                dots_txt=File(f,name=r_zone_file_path.name),
                conteudo=output_string,
                local_dots_url=str(save_path)
            )
            new_red_zone.save()
            f.close()
        serializer = red_zone_serializer(new_red_zone)
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
        # Pega a timestamp do começo do mês do passado e pesquisa no banco
        stamp = time_past.replace(day=1, hour=0, minute=0, second=0, microsecond=0).timestamp()
        alerts = alert.objects.filter(timestamp__gte=stamp)
        # alerts.filter() -> filtra mais
        serializer = alert_serializer(alerts, many=True)
        months = {"01": "Janeiro/", "02": "Fevereiro/", "03": "Março/",
                  "04": "Abril/", "05": "Maio/", "06": "Junho/",
                  "07": "Julho/", "08": "Agosto/", "09": "Setembro/",
                  "10": "Outubro/", "11": "Novembro/", "12": "Dezembro/"}
        now_month = months[str(time_now)[5:7]] + str(time_now)[:4]
        past_month = months[str(time_past)[5:7]] + str(time_past)[:4]
        # Dicts com os dados que serão usados no front. Começam zerados e acrescenta conforme avalia os alertas
        today = {"month": "Hoje", "total": 0, "EPI": 0, "red_zone": 0, "approved": 0, "disapproved": 0}
        now_monthly = {"month": now_month, "total": 0, "EPI": 0, "red_zone": 0, "approved": 0, "disapproved": 0}
        past_monthly = {"month": past_month, "total": 0, "EPI": 0, "red_zone": 0, "approved": 0, "disapproved": 0}
        # Avalia os alertas:
        # Se for o ano-mês (2022-02) da data atual for igual ao 'date_added' do alerta, então irá verificar,
        # Se o dia for igual ao de hoje ele atualiza os dicts de hoje e do mês atual,
        # Caso contrário irá atualizar somente o dict do mês atual
        for alert_ in serializer.data:
            if alert_["date_added"][:7] == str(time_now)[:7]:
                now_monthly["total"] += 1
                if alert_["date_added"][:10] == str(time_now)[:10]:
                    today["total"] += 1
                    if alert_["get_category_name"].lower() == "nonconformity":
                        today["EPI"] += 1
                        now_monthly["EPI"] += 1
                    elif alert_["get_category_name"].lower() == "redzone":
                        today["red_zone"] += 1
                        now_monthly["red_zone"] += 1
                    if alert_["thumb_up"]:
                        today["approved"] += 1
                        now_monthly["approved"] += 1
                    elif alert_["thumb_down"]:
                        today["disapproved"] += 1
                        now_monthly["disapproved"] += 1
                else:
                    if alert_["get_category_name"].lower() == "nonconformity":
                        now_monthly["EPI"] += 1
                    elif alert_["get_category_name"].lower() == "redzone":
                        now_monthly["red_zone"] += 1
                    if alert_["thumb_up"]:
                        now_monthly["approved"] += 1
                    elif alert_["thumb_down"]:
                        now_monthly["disapproved"] += 1
            # Se o ano e mês for igual ao do passado, atualiza o respectivo dict
            elif alert_["date_added"][:7] == str(time_past)[:7]:
                past_monthly["total"] += 1
                if alert_["get_category_name"].lower() == "nonconformity":
                    past_monthly["EPI"] += 1
                elif alert_["get_category_name"].lower() == "redzone":
                    past_monthly["red_zone"] += 1
                if alert_["thumb_up"]:
                    past_monthly["approved"] += 1
                elif alert_["thumb_down"]:
                    past_monthly["disapproved"] += 1
        # Salva os 3 dicts em um único dict e envia para o front
        result = {"today": today, "now": now_monthly, "past": past_monthly}
        return Response(result)
