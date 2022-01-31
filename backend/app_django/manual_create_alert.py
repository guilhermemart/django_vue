from .models import alert
from random import randint
from django.core.files.images import ImageFile
import os
from pathlib import Path

def create_alert(fields):  # fields capos do alerta nao padrões
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    path = os.path.join(BASE_DIR, "media", "uploads", "sauron_imagens", "n_avaliadas", "example.png")
    alerta_to_create = alert(
        quantidade=fields.get("quantidade", randint(1, 3)),
        description=fields.get("description", ""),
        thumb_up=fields.get("thumb_up", False),
        thumb_down=fields.get("thumb_down", False),
        image=ImageFile(open(fields.get("image_path", path))),
        local_image_url=fields.get("image_path", path)
    )
    alerta_to_create.save()


