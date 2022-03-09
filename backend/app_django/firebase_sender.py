import pyrebase
import os
from datetime import datetime
import pytz
import requests
from .models import alert

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
firebase = ""
db = ""
storage = ""

def initialize_firebase_db():
    global firebase
    global db
    global storage
    if (firebase and db and storage) == "":
        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()
        storage = firebase.storage()


# cia -> nome da empresa para ser salvo no banco
# timestamp -> timestamp do alerta, será convertido em date time e usado como referência no firebase
# alerta -> dict do alerta
def firebase_uploader(cia, timestamp, alerta):
    global firebase
    global db
    global storage
    date_tm = datetime.fromtimestamp(int(timestamp/1000), pytz.timezone("Brazil/East"))
    # Tenta enviar a imagem
    firebase_image_url = upload_image(cia, date_tm, alerta["get_image"])
    if type(firebase_image_url) == type("s") and len(firebase_image_url) > 30:
        # Se a resposta de certo então salva a url no alerta atual e no alerta do banco local
        alerta["firebase_image_url"] = firebase_image_url
        alert_from_db = alert.objects.filter(id=alerta["id"])[0]
        alert_from_db.firebase_image_url = firebase_image_url
        alert_from_db.save()
        alerta["date"] = {"%date": alerta["date_added"]}
        alerta.pop("date_added")
        alerta["timestamp"] = {"%numberLong": alerta["timestamp"]}
        alerta["alerts"] = {alerta["get_category_name"]: alerta["quantidade"]}
        alerta.pop("quantidade", "get_category_name")
        db.child(cia).child("date-index/" + date_tm.strftime("%d-%m-%Y")).set(True)
        # Verifica se o "thumb_up" do alerta é True ou False e envia pra salvar na pasta approved/disapproved
        if (alerta["thumb_up"] == True):
            db.child(cia).child("approved").child("%04d" % date_tm.year).child("%02d" % date_tm.month) \
                .child("%02d" % date_tm.day).child(date_tm.strftime("%H:%M:%S,%f tz:%Z")).set(alerta)
            db.child(cia).child("disapproved").child("%04d" % date_tm.year).child("%02d" % date_tm.month) \
                .child("%02d" % date_tm.day).child(date_tm.strftime("%H:%M:%S,%f tz:%Z")).remove()
        elif (alerta["thumb_up"] == False):
            db.child(cia).child("disapproved").child("%04d" % date_tm.year).child("%02d" % date_tm.month) \
                .child("%02d" % date_tm.day).child(date_tm.strftime("%H:%M:%S,%f tz:%Z")).set(alerta)
            db.child(cia).child("approved").child("%04d" % date_tm.year).child("%02d" % date_tm.month) \
                .child("%02d" % date_tm.day).child(date_tm.strftime("%H:%M:%S,%f tz:%Z")).remove()

    return "Sucesso Dev!"


# cia -> nome da empresa para ser o nome da pasta
# timestamp -> timestamp do alerta, usa para ter o ano/mês do alerta e usar no nome da pasta
# image_path -> caminho da imagem com o url do django ('http://192.168.0.46:8000/media/imagem.png')
def upload_image(cia, dt, image_path):
    # Pega o caminho do arquivo a partir da home
    response = requests.get(image_path)
    image_path = os.path.expanduser(f"~{response.request.path_url}")
    # Pega somente o nome do arquivo
    image_name = image_path.split("/")
    image_name = image_name[len(image_name) - 1]
    # Salva no storage 'cia/nome_do_arquivo/ano/mes'
    storage_path = f"Alerts_{cia}/{dt.year}/{dt.month}/{image_name}"
    storage.child(storage_path).put(image_path)
    # Retorna a url da imagem
    return storage.child(storage_path).get_url(None)

# Tenta upar os alertas pendentes. Chama a função de upar para cada alerta
def retry_upload(alerts):
    for alert in alerts:
        attempt = firebase_uploader("Valaris", alert["timestamp"], alert)
        if attempt != "Sucesso Dev!":
            print("Não foi possível enviar alguns alertas pendentes para o Firebase")
            break


if __name__ == '__main__':
    print("a")