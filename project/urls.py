"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from project.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', contadoresAdmin), 
    path('admin/', admin.site.urls),
    path('appPartido/', include('appPartido.urls')),
    path('appEquipo/', include('appEquipo.urls')),
    path('jugador/<str:alias>', contextoJugador), 
    path('equipo/<str:nombre_equipo>', contextoEquipo),
    path('competencias/', contextoCompetencias),
    path('competenciasVivo/', contextoCompetenciasVivo),
    path('competencias/futbol/<str:nombre_competicion>', contextoCompetenciasFutbol),
    path('contacto', contextoContacto),
    path('tvVivo/<int:id>', contextoTVvivo),
    path('tvHome/encuentrosVivo/<int:idCompeticion>/', contextoTVhomeVivo, name='encuentros_por_jugar'),
    path('tvHome/encuentros/<int:idCompeticion>/', contextoTVhome, name='encuentros'),
    path('tvHome/<int:id>/', contextoTVhomeEncuentro, name='contextoTVhomeEncuentro'),
    path('datostv/', obtener_eventos_ajax),
    path('admintv/EnJuego/<int:idEncuentro>/',mostrarEvento , name='mostrar_evento'),
    path('admintv/encuentros', mostrarEncuentrosEvento, name='mostrar_encuentro_evento'),
    path('limpiar-eventos-temporales/', limpiar_eventos_temporales, name='limpiar_eventos_temporales'),
    path('admintv/generales/<int:idEncuentro>/',mostrarEventosGenerales , name='mostrar_eventos_generales'),
    path('competencias/<str:nombre_competicion>/fixture',contextoFixtureCompetencia),
    path('competencias/<str:nombre_competicion>/encuentros',contextoEncuentros),
    # path('competencias/<str:nombre_competicion>/lista_jugadores_amarillas',contextoListaJugadoresPorAmarillas),
    # path('competencias/<str:nombre_competicion>/lista_jugadores_rojas',contextoListaJugadoresPorRojas),
    path("tabla-posiciones/<str:nombre_competicion>",contextoTablaPosiciones),
    path("reporte/sedes", contextoSedes, name="sedes/filtrar"),
    path("reporte/organizaciones", contextoOrganizaciones, name="filtrar/organizaciones"),
    path('reporte_tabla_posiciones/<str:nombre_competicion>/', contextoTablaPosiciones),
    path('sede/detalle/<int:sede_id>/', detalle_sede, name='detalle_sede'),
    path('reporte/equipos/', lista_equipos_por_competicion_y_fase, name='lista_equipos'),
    path('cambiar_estado_encuentro_E/', cambiar_estado_encuentro_E, name='cambiar_estado_encuentro_E'),
    path('cambiar_estado_encuentro_F/', cambiar_estado_encuentro_F, name='cambiar_estado_encuentro_F'),
    path('reporte/personas/', lista_personas_por_tipo, name='lista_personas'),
    path('reporte/jugadores', reporte_jugadores, name='reporte_jugadores'),
    #Esta si se puede eliminar
    path('reporte/organizacion', contextotablaorganizacion, name='lista_organizacion'),
    #
    path('reporte/organizacion/<int:orga_id>', contextotablaorganizacionindi, name='lista_organizacion_indi'),
    path('apicompetenciasequipo/<str:nombre_competicion>/', apicompetenciasequipo, name='apicompetenciasequipo'),
    path('apitarjetas/<int:tipo>/<int:idContrato>/', infracciones, name='apitarjetas'),
    path('actualizar_cronometro/', actualizar_cronometro, name='actualizar_cronometro'),
    path('obtener_cronometro/', obtener_hora_actual, name='obtener_cronometro'),
    # path('futbol/tv/<int:id>',contextoTv),
    path("futbol/sedes", contextoSedes),
    # path("futbol/tv/<int:id>", contextoTv),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", index),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
