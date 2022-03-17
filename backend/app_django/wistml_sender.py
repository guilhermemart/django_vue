import os
import base64
import requests
from .models import alert
from .serializers import alert_serializer

fake_alert = {  # usado para testes
    'alert_category': {'name': 'Nonconformity'},
    'identificador': "example",
    'sequencial': '0',
    'slug': "alerta_example",
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


def compose_witsml(alerta=None):
    if alerta is None:
        alerta = fake_alert
    with open(os.path.join(os.getcwd(), "witsml_models", 'opsreport.xml')) as input_ops:
        string_ops = input_ops.read()
    input_ops.close()
    output_ops = string_ops.replace('%uidOps', f"Alert_{alerta['sequencial']}")
    output_ops = output_ops.replace('%opsName', f"PPE/RedZone_Alert_{alerta['sequencial']}")
    output_ops = output_ops.replace('%dTim', f"{alerta['date_added']}")
    output_ops = output_ops.replace('%comments', f"{alerta['get_category_name']} :{alerta['quantidade']}")
    '''
    # removido backup do opsreport witsml --> poupa memoria de armazenamento
    with open(os.path.join(os.getcwd(), "witsml_models", f"{alerta['sequencial']}_opsreport.xml"), 'w') as out_ops:
        out_ops.write(output_ops)
    out_ops.close()'''
    with open(os.path.join(os.getcwd(), "witsml_models", 'attachment.xml')) as input_att:
        string_att = input_att.read()
    input_att.close()
    image = open(alerta['get_image'], 'rb')
    image_64_encode = base64.b64encode(image.read())  # witsml exige base64 nas imagens
    output_att = string_att.replace('%uid_attach', f"Alert_{alerta['sequencial']}")
    output_att = output_att.replace('%name_attach', f"PPE/RedZone_Alert_{alerta['sequencial']}")
    output_att = output_att.replace('%filename', f"attachment{alerta['sequencial']}.jpg")
    output_att = output_att.replace("%image", str(image_64_encode).replace("b'","").replace("'", ""))
    '''
    # Removido backup do attachment witsml --> poupa memoria de armazenamento
    with open(os.path.join(os.getcwd(), "witsml_models", f"{alerta['sequencial']}_attachment.xml"), 'w') as out_att:
        out_att.write(output_att)
    out_att.close()'''
    with open(os.path.join(os.getcwd(), "witsml_models", 'getcap.xml')) as input_getcap:
        string_getcap = input_getcap.read()  # le um model de getcap --> usado para verificar funcionalidade do servidor
    input_getcap.close()
    return output_ops, output_att, string_getcap


def send_witsml(witsml_user, witsml_pass, url, alerta):
    data = compose_witsml(alerta)
    headers_getcap = {  # envia um request pro servidor e verifica suas funcionalidades
        'Content-Type': 'text/xml',
        'SOAPAction': 'http://www.witsml.org/action/120/Store.WMLS_GetCap',
        'Authorization': get_witsml_pass(witsml_user, witsml_pass)
    }
    response = requests.request("POST", url, headers=headers_getcap, data=data[2])
    print(response.text)
    if "Function completed successfully" in response.text:  # resposta positiva, servidor funcionando
        headers = {
            'Content-Type': 'text/xml',
            'SOAPAction': 'http://www.witsml.org/action/120/Store.WMLS_AddToStore',
            'Authorization': get_witsml_pass(witsml_user, witsml_pass)
        }
        '''
        # removido a tentativa inicial --> direto pro looping de envio da pilha
        # uma busca a menos no bd
        print("Sending opsReport (1)")
        response_ops = requests.request("POST", url, headers=headers, data=data[0])
        print("Sending attachment (1)")
        response_att = requests.request("POST", url, headers=headers, data=data[1])
        alert_to_update = alert.objects.filter(identificador=alerta.identificador)[0]
        alert_to_update.witsml_confirm = "sent"
        alert_to_update.save()'''
        # Procura os alertas que não foram enviados
        alerts_not_sent = alert.object.filter(witsml_confirm="witsml_not_sent")
        # Chama a função de enviar para cada alerta -- nao tenta enviar mais de uma vez
        for alert_ in alerts_not_sent:  # tentativa de esvaziar a pilha de alertas nao enviados
            #  tudo que enviar aqui é lucro
            alert_to_retry = alert_serializer(alert_).data
            data = compose_witsml(alert_to_retry)
            response = requests.request("POST", url, headers=headers_getcap, data=data[2])
            if "Function completed successfully" in response.text:  # resposta positiva, servidor funcionando
                print("Sending opsReport")
                response_ops = requests.request("POST", url, headers=headers, data=data[0])
                print("Sending attachment")
                response_att = requests.request("POST", url, headers=headers, data=data[1])
                alert_.witsml_confirm = "sent"
                alert_.save()
            else:
                break  # perdeu contato com o servidor
    else:
        return "Error"


def get_witsml_pass(user, password):
    base64_out = base64.b64encode(f"{user}:{password}".encode("ascii"))
    return 'Basic ' + str(base64_out)[2:-1]
