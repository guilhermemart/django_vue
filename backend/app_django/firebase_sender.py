import io
import urllib.request

import PIL.Image
import PIL.ImageQt
import pyrebase
import os
from datetime import datetime
import pytz
import requests

dir_path = os.path.dirname(os.path.realpath(__file__))
json_ = os.path.join(dir_path, "django-test-de-firebase.json")

firebaseConfig = {
    "apiKey": "apiKey",
    "authDomain": "django-test-de.firebaseapp.com",
    "databaseURL": "https://django-test-de-default-rtdb.firebaseio.com",
    "projectId": "django-test-de",
    "storageBucket": "django-test-de.appspot.com",
    "serviceAccount": json_
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
storage = firebase.storage()


# cia -> nome da empresa para ser salvo no banco
# date_tm -> datetime do alerta, será usado como ponto de referência para depois localizar o alerta no banco
# alerta -> dict do alerta
def firebase_uploader(cia, date_tm, alerta):
    # Baseado no exemplo de referência, ele muda o "date_added" para "date"
    alerta["date"] = {"%date": alerta["date_added"]}
    alerta.pop("date_added")
    alerta["timestamp"] = {"%numberLong": alerta["timestamp"]}
    alerta["alerts"] = {alerta["get_category_name"]: alerta["quantidade"]}
    alerta.pop("quantidade", "get_category_name")
    # Utiliza o date_tm como referência
    db.child(cia).child("date-index/" + date_tm.strftime("%d-%m-%Y")).set(True)
    # Verifica se o "thumb_up" do alerta é True ou False e envia pra salvar na pasta approved/disapproved
    if (alerta["thumb_up"] == True):
        db.child(cia).child("approved").child("%04d" % date_tm.year).child("%02d" % date_tm.month)\
            .child("%02d" % date_tm.day).child(date_tm.strftime("%H:%M:%S,%f tz:%Z")).set(alerta)
        db.child(cia).child("disapproved").child("%04d" % date_tm.year).child("%02d" % date_tm.month)\
            .child("%02d" % date_tm.day).child(date_tm.strftime("%H:%M:%S,%f tz:%Z")).remove()
    elif (alerta["thumb_up"] == False):
        db.child(cia).child("disapproved").child("%04d" % date_tm.year).child("%02d" % date_tm.month)\
            .child("%02d" % date_tm.day).child(date_tm.strftime("%H:%M:%S,%f tz:%Z")).set(alerta)
        db.child("valaris").child("approved").child("%04d" % date_tm.year).child("%02d" % date_tm.month)\
            .child("%02d" % date_tm.day).child(date_tm.strftime("%H:%M:%S,%f tz:%Z")).remove()

    return "Sucesso Dev!"

# cia -> nome da empresa para ser o nome da pasta
# image_path -> caminho da imagem com o url do django ('http://192.168.0.46:8000/media/imagem.png')
def upload_image(cia, image_path):
    # Tentativa de dar put usango a string toda, incluindo o IP do django
    # No momento não consegui fazer desse jeito
    """response = requests.get(image_path)"""
    # Então no momento estou cortando o IP da string
    image_path = os.path.expanduser(f"~/{image_path[25:]}")
    # Pega somente o nome do arquivo
    image_name = image_path.split("/")
    image_name = image_name[len(image_name) - 1]
    # Salva no storage 'cia/nome_do_arquivo'
    cloud_path = storage.child(f"{cia}/{image_name}")
    cloud_path.put(image_path)
    # Não consigo retornar o url dentro da função, diz que é "NoneType" se tento pegar aqui
    # Pegar o url fora dessa função, talvez outra função só pra isso. Chamar a função no fim dessa, talvez


if __name__ == '__main__':
    # Dados para um teste básico
    date = datetime.now(pytz.timezone("Brazil/East"))
    dict = {'id': 8,
            'identificador': '1644958651892',
            'timestamp': 1612143950000,
            'date_added': '2022-02-15T17:57:31.893109-03:00',
            'anotacoes': '',
            'quantidade': 2,
            'thumb_up': False,
            'thumb_down': True,
            'get_image': 'http://192.168.0.46:8000/media/uploads/sauron_imagens/n_avaliadas/example_c0wEALQ.png',
            'get_thumbnail': 'http://192.168.0.46:8000/media/uploads/sauron_thumbnails/example_c0wEALQ.png',
            'firebase_image_url': 'image_not_sent',
            'get_absolute_url': '/Nonconformity/example_1644958651892/',
            'local_image_url': '/home/devanir/media/uploads/sauron_imagens/n_avaliadas/example.png',
            'get_opsreport': 'http://192.168.0.46:8000/media/witsml/opsreport.xml',
            'get_attachment': 'http://192.168.0.46:8000/media/witsml/attachment.xml',
            'sequencial': 5,
            'witsml_confirm': 'witsml_not_sent',
            'get_category_name': 'nonconformity'
            }
    #firebase_uploader("Testing", date, dict)

    # Printa os arquivos do storage
    files = storage.list_files()
    for i in files:
        print(i.name)
    #print(os.path.expanduser(f"~/{dict['get_thumbnail'][25:]}"))
    #storage.child("Valaris/teste").put(os.path.expanduser(f"~/{dict['get_thumbnail'][25:]}"))
    #print(storage.child("Harpia/harpias.webp").get_url(None))


    # Rodando esse arquivo faz com que seja upado e printa o link da imagem
    upload_image("testFolder", dict["get_thumbnail"])
    print(storage.child("testFolder/example_c0wEALQ.png").get_url(None))