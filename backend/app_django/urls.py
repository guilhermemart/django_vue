from django.urls import path, include

from . import views

urlpatterns = [
    path('latest-alerts/<int:page>', views.latest_alerts_list.as_view()),
    path('update_alert_by_identificador/', views.update_alert.as_view()),
    path('create_alert/', views.create_alert.as_view()),
]
'''path('products/search/', views.search),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),'''
# no django <tipodavariavel:nomedavariavel> é aplicado em todos os metodos que usem (nomedavariavel) 
# da classe chamada