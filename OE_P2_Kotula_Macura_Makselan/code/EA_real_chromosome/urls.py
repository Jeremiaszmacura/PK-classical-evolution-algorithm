from django.urls import path

from . import views

urlpatterns = [
    path('', views.EA_real_chromosome_api)
]
