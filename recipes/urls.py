# recipes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("planejamentomt/", views.planejamentomt, name="planejamentomt"),
    path("planejamentomt/correcao-correntes/", views.correcao_correntes, name="correcao_correntes"),
]

