from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('faq/', views.faq, name="faq"),
    path('perfil/', views.perfil, name="perfil"),
    path('salas/', views.salas, name="salas"),
    path('detalhes/', views.detalhes, name='detalhes'),
]
