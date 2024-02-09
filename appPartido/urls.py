from django.urls import path 
from .views import *


urlpatterns = [
    path('get_encuentros/', ObtenerEncuentrosView.as_view(), name='get_encuentros'),
    path('get_alineaciones/', ObtenerAlineacionesView.as_view(), name='get_alineaciones'),
    path('lista_encuentros/', mostrarEncuentros, name='lista_encuentros'),
    path('asignar/alineaciones/<int:encuentro_id>/', asignarAlineacion, name='asignarAlineaciones'),
    path('asignar/estadisticas/<int:encuentro_id>/', asignarEstadisticas, name='asignarEstadisticas'),
    path('asignar/terna_arbitral/<int:encuentro_id>/', asignar_terna_arbitral, name='asignar_terna_arbitral'),
    path('asignar/eventos/<int:encuentro_id>/', asignarEventos, name='asignarEventos'),
    path('asignar/<str:tipo>/<int:encuentro_id>/', asignar, name='asignar'),
]



