from .app_django.models import alert
from .app_django.serializers import alert_serializer
from shutil import move, copy


def update_alert_by_id(request):  # passar o id no data do POST
    _id = request.data.get('id')
    alerta_to_modify = alert.objects.get(id=_id)
    # cuidando dos thumbs
    thumb_up = request.data.get('thumb_up', alerta_to_modify.thumb_up)
    thumb_down = request.data.get('thumb_down', alerta_to_modify.thumb_down)
    alerta_to_modify.thumb_up = bool(thumb_up)
    alerta_to_modify.thumb_down = bool(thumb_down)
    # cuidando da imagem
    old_image_url = alerta_to_modify.image.url
    if thumb_up and thumb_down:
        alerta_to_modify.image.url = alerta_to_modify.image.url.replace('thumb_up', 'n_avaliadas').replace('thumb_down', 'n_avaliadas')
    elif thumb_up:
        alerta_to_modify.image.url = alerta_to_modify.image.url.replace('n_avaliadas', 'thumb_up').replace('thumb_down', 'thumb_up')
    elif thumb_down:
        alerta_to_modify.image.url = alerta_to_modify.image.url.replace('n_avaliadas', 'thumb_down').replace('thumb_up', 'thumb_down')
    else:
        alerta_to_modify.image.url = alerta_to_modify.image.url.replace('thumb_up', 'n_avaliadas').replace('thumb_down', 'n_avaliadas')
    move(old_image_url, alerta_to_modify.image.url)
    # cuidando das notes
    notes = request.data.get('notes', "")
    alerta_to_modify.description = alerta_to_modify.description + "\n" + notes
    alerta_to_modify.save()
    alerta_serializado = alert_serializer(alerta_to_modify)
    print(alerta_serializado)
    '''temp["thumb_up"] = str(thumb_up).lower()
    temp["thumb_down"] = str(thumb_down).lower()
    image_url_primaria = temp['imageUrl'].replace("/thumb_up", "").replace("/thumb_down", "")
    # a condicional a seguir é para caso se deseje acabar com o backup
    if os.path.isfile(temp['imageUrl']):  # verifica se a imagem existe
        old_image_url = temp['imageUrl']
    else:  # procura no caminho raiz (backup) a imagem correspondente
        old_image_url = image_url_primaria
    image_url_primaria_splited = image_url_primaria.split("/")
    if thumb_up:
        new_url = "/".join(image_url_primaria_splited[:-1]) + "/thumb_up/" + image_url_primaria_splited[-1]
        if not os.path.isdir("/".join(image_url_primaria_splited[:-1]) + "/thumb_up/"):
            os.mkdir("/".join(image_url_primaria_splited[:-1]) + "/thumb_up/")
        move(old_image_url, new_url)
        copy(new_url, image_url_primaria)  # se quiser evitar duas imagens comente essa linha
        temp['imageUrl'] = new_url
    elif thumb_down:
        if not os.path.isdir("/".join(image_url_primaria_splited[:-1]) + "/thumb_down/"):
            os.mkdir("/".join(image_url_primaria_splited[:-1]) + "/thumb_down/")
        new_url = "/".join(image_url_primaria_splited[:-1]) + "/thumb_down/" + image_url_primaria_splited[-1]
        move(old_image_url, new_url)
        copy(new_url, image_url_primaria)
        temp['imageUrl'] = new_url
    else:
        new_url = image_url_primaria
        temp['imageUrl'] = new_url
        move(old_image_url, new_url)  # /home/sauron/output-sauron/thumb_up_down --> /home/sauron/output-sauron
    temp["seen"] = True
    try:
        # parte do firebase
        img_name = datetime.utcfromtimestamp(int(temp['timestamp'] / 1000))
        gcs.upload_blob('harpia-projetos.appspot.com', new_url,
                        'Alerts_teste_' + cia + '/' + str(img_name.year) + '/' + str(img_name.month) + '/' + str(
                            temp['_id']))
        firebase_img_url = gcs.make_blob_public('harpia-projetos.appspot.com',
                                                'Alerts_teste_' + cia + '/' + str(img_name.year) + '/' + str(
                                                    img_name.month) + '/' + str(temp['_id']))
        temp['firebase_img_url'] = firebase_img_url
    except Exception as e:
        print(f"{e} Problemas para atualizar alert images no Firebase")
        firebase_img_url = '%img_not_found%'
        temp['firebase_img_url'] = firebase_img_url
    if "_id" not in temp:
        temp["_id"] = dados["_id"]
    try:
        enviar_dados(cia, str(temp['thumb_up']).lower(),
                     datetime.fromtimestamp(int(temp['timestamp'] / 1000), pytz.timezone("Brazil/East")), temp)
    except Exception as e:
        print(f"Erro: {e} - impossível enviar dados para o firebase")
    try:
        db.alerts.update_many({"_id": ObjectId(idd)}, {"$set": {"imageUrl": temp['imageUrl']}})
        db.alerts.update_many({"_id": ObjectId(idd)}, {"$set": {"thumb_up": temp['thumb_up']}})
        db.alerts.update_many({"_id": ObjectId(idd)}, {"$set": {"thumb_down": temp['thumb_down']}})
        db.alerts.update_many({"_id": ObjectId(idd)}, {"$set": {"firebase_img_url": temp['firebase_img_url']}})
    except Exception as e:
        db.alerts.delete_one({"_id": temp["_id"]})
        db.alerts.insert_one(temp)
        print(f"{e} Problemas para atualizar alertas")
    response.set_header("Content-Type", "application/json")
    response.set_header("Cache-Control", 'no-cache')
    response.add_header("Cache-Control", "no-store")
    response.add_header("Cache-Control", 'must-revalidate')
    response.add_header("Acces-Control-Allow-Origin", '*')
    client.close()
    return json.dumps(temp, default=json_util.default)'''
