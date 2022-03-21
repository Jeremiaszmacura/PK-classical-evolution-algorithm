from django.urls import path

from . import views


urlpatterns = [
    path('', views.classic_EA_api)
]
