from django.shortcuts import redirect
from decouple import Config, RepositoryEnv, AutoConfig
import os

ENV_File = os.path.dirname(os.path.abspath(__file__))
config = Config(RepositoryEnv(ENV_File + "/.env"))


def url_redirect_alert(request, category, alert):
    print(alert)
    return redirect("http://" + config.get("LOCAL_IP") + f":8080/{category}/{alert}")


def url_redirect_category(request, category):
    print(category)
    return redirect("http://" + config.get("LOCAL_IP") + f":8080/{category}")


def url_redirect_redzone(request, camera, red_zone):
    print(red_zone)
    return redirect("http://" + config.get("LOCAL_IP") + f":8080/red_zone/{camera}/{red_zone}")


def url_redirect_camera(request, camera):
    print(camera)
    return redirect("http://" + config.get("LOCAL_IP") + f":8080/red_zone/{camera}")


def url_redirect_home(request):
    return redirect("http://" + config.get("LOCAL_IP") + ":8080/log-in")
