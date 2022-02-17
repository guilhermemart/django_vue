from .models import alert
from .serializers import alert_serializer
from shutil import move, copy


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

