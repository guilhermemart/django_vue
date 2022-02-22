from rest_framework import serializers
from .models import alert, category, camera, red_zone


class alert_serializer(serializers.ModelSerializer):
    class Meta:
        model = alert
        fields = (
            "id",  # mesma do mongo se possível
            "identificador",  # valor pra achar o alerta especifico
            "timestamp",  # formato js
            "date_added",  #
            "anotacoes",  # fogo pessoa epi redzone veiculo
            "quantidade",  # dificilmente mais de 1 por imagem
            "thumb_up",  # avaliado positivo
            "thumb_down",  # avaliado falso positivo
            "get_image",  # url da imagem localmente
            "get_thumbnail",  # url imagem local reduzida
            "firebase_image_url",  # qdo alerta é criado a imagem é enviada para firebase
            "get_absolute_url",  # primeiro link da imagem (imutavel)
            "local_image_url",   # local que a imagem encontra agora
            "get_opsreport",
            'get_attachment',
            'sequencial',
            'witsml_confirm',
            'get_category_name'
        )


class category_serializer(serializers.ModelSerializer):
    alerts = alert_serializer(many=True)
    class Meta:
        model = category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "alerts",
        )


class red_zone_serializer(serializers.ModelSerializer):
    class Meta:
        model = red_zone
        fields = (
            "id",  # mesma do mongo se possível
            "identificador",  # valor pra achar o alerta especifico
            "timestamp",  # formato js
            "date_added",  #
            "name",  # ponte, guindaste ..
            "get_dots",  # retorna os pontos da red zone em formato txt
            "conteudo",  # retorna os pontos da red json
            "get_absolute_url",  # primeiro link da imagem (imutavel)
            "local_dots_url",   # local que o txt encontra agora
            "dots",
            "enabled",
            "get_camera"
        )


class camera_serializer(serializers.ModelSerializer):
    red_zones = red_zone_serializer(many=True)

    class Meta:
        model = camera
        fields = {
            "id",
            "name",
            "ativa",
            "get_absolute_url",
            "red_zones"
        }
