from django.shortcuts import redirect

def url_redirect(request, category, alert):
    print(alert)
    return redirect(f"http://127.0.0.1:8080/{category}/{alert}")