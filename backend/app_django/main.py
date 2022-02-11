from .models import alert
from .serializers import alert_serializer
from shutil import move, copy
import os
import base64
import requests

fake_alert={
    'alert_category' : {'name':'Nonconformity'},
    'identificador' : "example",
    'sequencial' : '0',
    'slug' : "alerta_example",
    'timestamp': 1643679950000 - (365 * 24 * 60 * 60 * 1000),
    'date_added': "2022-02-10T15:25:14-03:00",
    'anotacoes': "",
    'quantidade': 0,
    'thumb_up': False,
    'thumb_down': False,
    'get_image': 'witsml_models/example.jpg',
    'thumbnail': 'uploads/sauron_thumbnails/',
    'firebase_image_url': "replace_here_later_for_firebase_url",
    'local_image_url': "uploads/sauron_imagens/n_avaliadas/example.png",
    'opsreport': "witsml/opsreport.xml",
    'attachment': "witsml/attachment.xml",
    'witsml_confirm': 'witsml_not_sent'
}


def update_alert_by_identificador(request):  # passar o ident no data do POST
    _id = request.data.get('identificador')
    print(_id)
    alerta_to_modify = alert.objects.get(identificador=_id)
    # cuidando dos thumbs
    thumb_up = request.data.get('thumb_up', alerta_to_modify.thumb_up)
    thumb_down = request.data.get('thumb_down', alerta_to_modify.thumb_down)
    alerta_to_modify.thumb_up = bool(thumb_up)
    alerta_to_modify.thumb_down = bool(thumb_down)
    # cuidando da imagem
    old_image_url = alerta_to_modify.image.url
    if "n_avaliadas" not in old_image_url:
        path_splitado = old_image_url.split(sep="/")
        path_splitado = path_splitado.insert(-1, "n_avaliadas")
        copy(old_image_url, "/".join(path_splitado))
        old_image_url = "/".join(path_splitado)
    print(old_image_url)
    if thumb_up and thumb_down:  # true true nao pode
        new_image_url = old_image_url.replace("thumb_up","n_avaliadas").replace("thumb_down", "n_avaliadas")
    elif thumb_up:
        new_image_url = old_image_url.replace("n_avaliadas","thumb_up").replace("thumb_down", "thumb_up")
    elif thumb_down:
        new_image_url = old_image_url.replace("n_avaliadas","thumb_down").replace("thumb_up", "thumb_down")
    else:  # não avaliada ou desavaliada
        new_image_url = old_image_url.replace("thumb_up","n_avaliadas").replace("thumb_down", "n_avaliadas")
    print(new_image_url)
    alerta_to_modify.local_image_url = new_image_url
    # cuidando das notes
    notes = request.data.get('anotacoes', "")
    alerta_to_modify.anotacoes = alerta_to_modify.anotacoes + "\n" + notes
    alerta_to_modify.save()
    alerta_serializado = alert_serializer(alerta_to_modify)
    print(alerta_serializado)
    return alerta_to_modify


def compose_witsml(alerta=None):
    if alerta is None:
        alerta = fake_alert
    with open(os.path.join(os.getcwd(), "witsml_models", 'opsreport.xml')) as input_ops:
        string_ops = input_ops.read()
    input_ops.close()
    output_ops = string_ops.replace('%uidOps', f"Alert_{alerta['sequencial']}")
    output_ops = output_ops.replace('%opsName', f"PPE/RedZone_Alert_{alerta['sequencial']}")
    output_ops = output_ops.replace('%dTim', f"{alerta['date_added']}")
    output_ops = output_ops.replace('%comments', f"{alerta['alert_category']['name']} :{alerta['quantidade']}")
    with open(os.path.join(os.getcwd(), "witsml_models", 'temp_opsreport.xml'), 'w') as out_ops:
        out_ops.write(output_ops)
    out_ops.close()
    with open(os.path.join(os.getcwd(), "witsml_models", 'attachment.xml')) as input_att:
        string_att = input_att.read()
    input_att.close()
    image = open(alerta['get_image'], 'rb')
    image_64_encode = base64.b64encode(image.read())
    output_att = string_att.replace('%uid_attach', f"Alert_{alerta['sequencial']}")
    output_att = output_att.replace('%name_attach', f"PPE/RedZone_Alert_{alerta['sequencial']}")
    output_att = output_att.replace('%filename', f"attachment{alerta['sequencial']}.jpg")
    output_att = output_att.replace("%image", str(image_64_encode).replace("b'","").replace("'", ""))
    with open(os.path.join(os.getcwd(), "witsml_models", 'temp_attachment.xml'), 'w') as out_att:
        out_att.write(output_att)
    out_att.close()
    return alerta['thumb_up']


def send_witsml(witsml_user, witsml_pass, url, data):
    headers = {
        'Content-Type': 'text/xml',
        'SOAPAction': 'http://www.witsml.org/action/120/Store.WMLS_AddToStore',
        'Authorization': get_witsml_pass(witsml_user, witsml_pass)
    }
    resposta = requests.request("POST", url, headers=headers, data=data)


def get_witsml_pass(user, password):
    base64_out = base64.b64encode(f"{user}:{password}".encode("ascii"))
    return 'Basic ' + str(base64_out)[2:-1]