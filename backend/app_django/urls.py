from django.urls import path, include


from . import views

urlpatterns = [
    path('latest-alerts/<int:page>', views.latest_alerts_list.as_view()),
    path('update_alert_by_identificador/', views.update_alert.as_view()),
    path('create_alert/', views.create_alert.as_view()),
    path('alerts/<slug:category_slug>/<slug:alert_slug>/', views.alert_detail.as_view()),
    path('loaddots/<slug:camera_slug>', views.load_red_zone.as_view()),
    path('loaddots_ativos/<slug:camera_slug>', views.load_red_zone.as_view()),
    path('alert_search/<int:init>/<int:end>/<int:page>', views.alert_search.as_view())
]
'''path('products/search/', views.search),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),'''
# no django <tipodavariavel:nomedavariavel> é aplicado em todos os metodos que usem (nomedavariavel) 
# da classe chamada