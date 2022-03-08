from django.urls import path, include


from . import views

urlpatterns = [
    path('latest-alerts/<int:page>', views.latest_alerts_list.as_view()),
    path('update_alert_by_identificador/', views.update_alert.as_view()),
    path('create_alert/', views.create_alert.as_view()),  # cria um alerta falso ou não
    path('alerts/<slug:category_slug>/<slug:alert_slug>/', views.alert_detail.as_view()),  # detalhes de um alerta
    path('alerts/report/', views.alerts_report.as_view()),  # para o resumo de alertas
    path('deldots/<red_zone_name>', views.del_red_zone.as_view()),
    path('update_red_zone/<red_zone_name>', views.update_red_zone.as_view()),
    path('save_red_zone/', views.save_red_zone.as_view()),
    path('watchdog/', views.wait_alert.as_view()),  # fica preso num for até chegar um alerta novo
    path('load_rz/<int:cam>', views.load_red_zones.as_view()),  # retorna as red zones de uma camera renderizadas como rzones
    path("red_zone/<slug:cam>", views.get_cam.as_view()),  # retorna uma camera e um array com suas red zones
    path('cameras/update/', views.update_cameras.as_view()),
    path('cameras/get_url/', views.get_url_cameras.as_view()),
]
'''path('products/search/', views.search),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),'''
# no django <tipodavariavel:nomedavariavel> é aplicado em todos os metodos que usem (nomedavariavel) 
# da classe chamada