from django.urls import path
from .views import *

urlpatterns = [
    path('get_contratos/', ObteneraJugadoresView.as_view(), name='get_contratos'),


]
