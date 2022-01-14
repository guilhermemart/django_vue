from django.shortcuts import render
from django.http import JsonResponse
from .get_alerts import get_alerts_by_page
# Create your views here.


def alerts(request):  # essa funcao será chamada no vue e posteriormente no django/index
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # se o request vem do vue
        return JsonResponse({'msg': 'teste do alerts no vue'})
    return render(request, '../templates/alerts.html', {'msg': 'teste do alerts no django'})