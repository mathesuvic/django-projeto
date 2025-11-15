from django.urls import path
#from django.contrib import admin
from recipes.views import home, contato, sobre


urlpatterns = [
    path('',home),
    path('sobre/',sobre),
    path('contato/',contato),
]