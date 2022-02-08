from django.shortcuts import redirect
# redirecionar as urls ṕadrão do django para o frontend


def url_redirect_alert(request, category, alert):
    print(alert)
    return redirect(f"http://127.0.0.1:8080/{category}/{alert}")


def url_redirect_category(request, category, alert):
    print(category)
    return redirect(f"http://127.0.0.1:8080/{category}")


def url_redirect_redzone(request, camera, red_zone):
    print(red_zone)
    return redirect(f"http://127.0.0.1:8080/red_zone/{camera}/{red_zone}")


def url_redirect_camera(request, camera):
    print(camera)
    return redirect(f"http://127.0.0.1:8080/red_zone/{camera}")


def url_redirect_home(request):
    return redirect(f"http://127.0.0.1:8080/log-in/")
