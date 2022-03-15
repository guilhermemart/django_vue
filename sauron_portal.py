from datetime import datetime
import requests
import json
'''funcionamento\n
colocar a lib na pasta do sauron\n 
executar a funcao enviar_alerta(argumentos)\n
com os 3 seguintes argumentos:\n
dict: the_alerta_dict \n
{\n
alert_category: "string_com_o_tipo_do_alerta",\n
timestamp: "int em ms de quando o alerta foi adquirido",\n
quantidade: "int quantidade de alertas daquele tipo na imagem",\n
local_image_url: "str path_da_imagem_no_computador_local"
}\n
backend_ip: str ip do computador que está rodando o harpia backend\n
backend_port: str porta destinada ao harpia backend\n
'''


global_token = ""

fake_alerta = {
    'local_image_url': "example.png",
    'alert_category': "nonconformity",
    'timestamp': int(datetime.now().timestamp()*1000),
    'quantidade': 1
}
ip = "10.0.2.15"
port = "8000"


def enviar_alerta(the_alerta, backend_ip=None, backend_port=None):
    """ Dados basicos a enviar no alerta \n
    alert_category = string com o nome da categoria ex: "nonconformity" \n
    timestamp = IntegerField (timestamp em milisegundos) \n
    quantidade = IntegerField(default=1) \n
    local_image_url = TextField(default="uploads/sauron_imagens/n_avaliadas/example.png")
    """
    global global_token
    if backend_ip is None:
        backend_ip = ip
    if backend_port is None:
        backend_port = port
    to_alert = {}
    for key in the_alerta:
        to_alert[key] = the_alerta[key]
    timestamp = datetime.now().timestamp()
    if the_alerta.get('timestamp', "error") != "error":  # tem o campo
        if int(the_alerta.get('timestamp', 0)) > timestamp:  # o campo esta em ms
            timestamp = int(the_alerta.get('timestamp', 0))
        else:
            timestamp = int(the_alerta.get('timestamp', 0) * 1000)
    else:
        timestamp = int(1000*timestamp)
    print("campo timestamp nao encontrado, usando atual")
    to_alert['alert_category'] = the_alerta.get("alert_category", 'not_defined')
    to_alert['identificador'] = the_alerta.get('identificador', f"sauron_{timestamp}")
    to_alert['timestamp'] = timestamp
    to_alert['quantidade'] = the_alerta.get('quantidade', 1)
    # analise dos thumbs transformando em bool
    to_alert['thumb_down'] = str(the_alerta.get('thumb_down', False)).lower() == 'true'
    to_alert['thumb_up'] = str(the_alerta.get('thumb_up', False)).lower() == 'true'
    # login no django rest
    url_do_django_token = f"http://{backend_ip}:{backend_port}/api/v1/token/login/"
    url_do_django_create = f"http://{backend_ip}:{backend_port}/api/v1/create_alert/"
    if global_token == "":
        formData = {
            "username": 'altave',
            "password": 'altave'
        }
        login = requests.post(url_do_django_token, data=formData)
        if login.json().get("auth_token", False) is not False:
            global_token = f"token {login.json().get('auth_token','')}"
        else:
            return "Problemas para acessar o backend"
    to_alert['Authorization'] = global_token
    #procura imagem localmente caso contrario usa exemplo
    local_image_url = the_alerta.get('local_image_url', "pwa_images/example.png")
    # ToDo substituir imagem exemplo por uma request
    img = open(local_image_url, 'rb')
    file = [('alert_image', img)]
    payload = to_alert
    result = requests.post(url_do_django_create, data=payload, files=file)
    img.close()
    if result.status_code == 200:
        print("alerta enviado com sucesso\nimagem armazenada no servidor")
        return "alerta enviado com sucesso\nimagem armazenada no servidor"
    else:
        print(f"alerta nao enviado erro: {result.text}")
        return f"alerta nao enviado erro: {result.text}"


def get_red_zones(cam, backend_ip=None, backend_port=None):
    """
    cam --> int [0, n_cameras[
    retorna um dict com todas as redzones da respectiva camera\n
     Obs: as cameras são representadas por inteiros iniciando no 0
     dict campos de maior interesse
     {'dots':[lista com tod os x, y's da red zone],
     'width': largura da imagem base,
     'height':altura da imagem base,
     'enabled': bool (red zone ativa, ou nao)
     .
     .
     .
     }
     """
    global global_token
    if backend_ip is None:
        backend_ip = ip
    if backend_port is None:
        backend_port = port
    url_do_django_token = f"http://{backend_ip}:{backend_port}/api/v1/token/login/"
    url_do_django_get_rz = f"http://{backend_ip}:{backend_port}/api/v1/load_rz/{cam}"
    if global_token == "":
        formData = {
            "username": 'altave',
            "password": 'altave'
        }
        login = requests.post(url_do_django_token, data=formData)
        if login.json().get("auth_token", False) is not False:
            global_token = f"token {login.json().get('auth_token', '')}"
        else:
            return "Problemas para acessar o backend"
    payload = {'Authorization': global_token}
    result = requests.get(url_do_django_get_rz, headers=payload)
    if result.status_code == 200:
        print(json.loads(result.text))
        return json.loads(result.text)
    else:
        print(f"rzs nao encontradas erro: {result.text}")
        return f"rzs nao encontradas erro: {result.text}"


def refresh_the_picture(cam, local_image_url="pwa_images/example.png", backend_ip=None, backend_port=None):
    ''' Le a URL da imagem local e envia pra camera correspondente no backend\
    cam = string camera ex: "cam0" Obs: inicia na cam0 \n
    local_image_url string path da imagem localmente ex: /home/user/sauron_images/example.png
    Return 200 se a imagem foi enviada, outro codigo != 200 se algo deu errado
    '''
    global global_token
    if backend_ip is None:
        backend_ip = ip
    if backend_port is None:
        backend_port = port
    img = open(local_image_url, 'rb')
    file = [('base_image', img)]
    url_do_django_token = f"http://{backend_ip}:{backend_port}/api/v1/token/login/"
    url_do_django_save_base_image = f"http://{backend_ip}:{backend_port}/api/v1/red_zone/camera/base_img_update/"
    if global_token == "":
        formData = {
            "username": 'altave',
            "password": 'altave'
        }
        login = requests.post(url_do_django_token, data=formData)
        if login.json().get("auth_token", False) is not False:
            global_token = f"token {login.json().get('auth_token', '')}"
        else:
            return "Problemas para acessar o backend"
    payload = {'Authorization': global_token, "camera": str(cam)}
    result = requests.post(url_do_django_save_base_image, data=payload, files=file)
    return result.status_code


if __name__ == "__main__":
    enviar_alerta(fake_alerta)
    #get_red_zones("0")
    #refresh_the_picture("cam2")
