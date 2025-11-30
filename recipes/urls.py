# recipes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("planejamentomt/", views.planejamentomt, name="planejamentomt"),
    path("capex/",views.capex, name="capex"),
    path("planejamentomt/correcao-correntes/", views.correcao_correntes, name="correcao_correntes"),
    path("capex/", views.capex, name="capex"),
    path("capex/<int:year>/", views.capex, name="capex_year"),
    path("capex/editar/<int:plan_id>/", views.capex_editar, name="capex_editar"),
    path("capex/editar/<int:plan_id>/<int:year>/", views.capex_editar, name="capex_editar_year"),
]

