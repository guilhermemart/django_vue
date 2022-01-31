from rest_framework import serializers
from .models import alert, category


class alert_serializer(serializers.ModelSerializer):
    class Meta:
        model = alert
        fields = (
            "id",  # mesma do mongo se possível
            "identificador",  # valor pra achar o alerta especifico
            "timestamp",  # formato js
            "date_added",  #
            "description",  # fogo pessoa epi redzone veiculo
            "quantidade",  # dificilmente mais de 1 por imagem
            "thumb_up",  # avaliado positivo
            "thumb_down",  # avaliado falso positivo
            "get_image",  # url da imagem localmente
            "get_thumbnail",  # url imagem local reduzida
            "firebase_image_url",  # qdo alerta é criado a imagem é enviada para firebase
            "get_absolute_url",  # primeiro link da imagem (imutavel)
            "local_image_url"   # local que a imagem encontra agora
        )


class CategorySerializer(serializers.ModelSerializer):
    alerts = alert_serializer(many=True)

    class Meta:
        model = category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "alerts",
        )
