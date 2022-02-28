from django.http import Http404
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
from django.core.files import File
import os
from pathlib import Path
# a lib pathlib funciona semelhante a os, mas o django se entende com ela
from datetime import datetime, timedelta, timezone
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

                # Procura os alertas que não foram enviados
                alerts_not_sent = alert.object.filter(witsml_confirm="witsml_not_sent")
                alerts = alert_serializer(alerts_not_sent, many=True).data
                # Chama a função de enviar para cada alerta
                for alert_ in alerts:
                    try:
                        send_witsml(config("WITSML_USER"), config("WITSML_PASS"), config("WITSML_URL"), alert_)
                    except Exception as e:
                        print(f"Erro ao tentar enviar alertas pendentes {e}")
                # Possivel problema: Esse campo 'witsml_confirm' do alerta acho que não muda depois de enviar,
                # então no momento acho que sempre tentaria enviar todos

            return Response(serializer.data)
        raise Http404


class create_alert(APIView):
    def create_category(self):
        new_category = category(
            name="fake_category"
        )
        new_category.save()
    # cria um novo alerta de acordo com os dados do request
    def get(self, request):
        # futuramente usar decouple para definir esse caminho
        path = Path().home().joinpath("media", "uploads", "sauron_imagens", "n_avaliadas", "example.png")
        simple_media_path = Path().joinpath("~", "media", "uploads", "sauron_imagens", "n_avaliadas", "example.png")
        fields = request.data
        category_name = fields.get('category_name', "fake_category")
        categoria_input = category.objects.filter(name=category_name)
        if categoria_input.count() > 0:
            categoria = categoria_input[0]
        else:
            self.create_category()
            categoria = category.objects.filter(name=category_name)
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
                local_image_url=fields.get("image_path", str(simple_media_path)),
                sequencial=int(alertas_qtde + 1),
                witsml_confirm="witsml_not_sent",
                timestamp= fields.get("timestamp", 1643679950000 - (365*24*60*60*1000) + randint(0,60*60*24*1000))
            )
            alerta_to_create.save()
            try:  # abre conexão com o bd pro pgpubsub perceber a chegada de um alerta novo
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
    # mostra uma pagina com a categoria, detalhes e alertas da categoria
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
        # cria a string que vai ser salva como txt
        output = request.data
        output_string = f"nome: {output['name']}, largura: {output['width']}, pontos: "
        for ponto in output["dots"]:
            output_string = output_string + str(ponto) + ","
        # caminho dos arquivos no settings django
        simple_save_path = os.path.join("~", "media", "uploads", "red_zones", "individual_red_zones", f"{output['name']}.txt")
        save_path = os.path.expanduser(os.path.join("~", "media", "uploads", "red_zones", "individual_red_zones", f"{output['name']}.txt"))
        save_path = request.data.get("red_zone_file_path", save_path)
        # precisa da lib Pathlib para salvar o arquivo
        path = Path().home().joinpath('media','uploads','red_zones','individual_red_zones',f'{output["name"]}.txt')
        with open(save_path, 'w') as rzone:
            rzone.write(output_string)
            rzone.close()
        camera_number = output['cam']
        wich_camera = camera.objects.filter(name="cam"+str(camera_number))[0]
        date_added = datetime.now(tz=timezone(timedelta(hours=-3)))
        ident = date_added.timestamp()
        r_zone_file_path = path  # r_zone_file_path = save_path nao aceitou o metodo File()
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
                local_dots_url=simple_save_path
            )
            new_red_zone.save()
            f.close()
        serializer = red_zone_serializer(new_red_zone)
        return Response(serializer.data)


class update_red_zone(APIView):
    def post(self, request, red_zone_name):
        rzone = red_zone.objects.filter(name=red_zone_name)[0]
        rzone.enabled = request.data['is_active'] == "true"
        rzone.save()
        serializer = red_zone_serializer(rzone)
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
        # Faz uma busca usando o timestamp do mês passado e faz outras buscas dentro dessa busca,
        # Busca com o timestamp desse mês e do dia de hoje, assim os alertas já ficam separados
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
