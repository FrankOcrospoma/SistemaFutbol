from calendar import c
from unittest import case
from django.forms import CharField
from django.shortcuts import get_object_or_404, render,redirect
from appContrato.models import *
# from bs4 import BeautifulSoup
from appEquipo.models import *
from appPartido.models import *
from appCompeticion.models import *
from django.views.decorators.csrf import csrf_exempt
from user.models import User
from django.db.models import *
from itertools import chain
from django.http import JsonResponse,HttpResponse
from django.templatetags.static import static
from django.forms.models import model_to_dict
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json
from operator import attrgetter
from django.contrib import messages
from collections import Counter

def contextoNav():
    
    deportes = deporte.objects.all()
    
    data ={
        'deportes' : deportes
    }

    return render ('header.html', data)
def contextoHeader():
    
    deportes = deporte.objects.all()
    
    data ={
        'deportes' : deportes,
        'competencias_nav': competicion.objects.all(),
    }

    return render ('header.html', data)

##
# def mostrarEvento(request):
    
#     eventos = evento.objects.all()
#     # evento_filtrado = evento.objects.filter(evento_id=eventos.evento_id).first()
    
#     # data_filtrada ={
#     #     'evento' : evento_filtrado
#     # }

#     data ={
#         'eventos' : eventos
#     }

#     return render (request,'moduloTV/evento.html', data)
##
# def mostrarEvento(request):
#     if request.method == 'POST':
#         eventos_seleccionados = request.POST.getlist('idEvento')
#         eventos = evento.objects.filter(evento_id__in=eventos_seleccionados)
#         #return JsonResponse({'eventos': list(eventos.values())})
#         # return render(request, 'tv.html', JsonResponse({'eventos': list(eventos.values())}))
#         obtener_eventos_ajax(eventos)    # Si el método no es POST, simplemente renderiza la página de eventos
    
#     eventos = evento.objects.all()
#     return render(request, 'moduloTV/evento.html', {'eventos': eventos})

# def obtener_eventos_ajax(eventos):
#     banners = []
#     #if eventos:
#     for evento in eventos:
#             banner = f'''<div class="banner-container">
#                 Tiempo: {evento.tiempo_reglamentario}
#                 </div>'''
#             banners.append(banner)
#     return JsonResponse({'banners': banners})
    
##

def contadoresAdmin(request):
    arbitros = persona.objects.filter(tipo_persona_id=3).count()
    entrenadores = persona.objects.filter(tipo_persona_id=2).count()
    jugadores = persona.objects.filter(tipo_persona_id=1).count()
    equipos = equipo.objects.count()
    usuarios = User.objects.all()
    data = {
        'arbitros' : arbitros,
        'entrenadores' : entrenadores,
        'jugadores' : jugadores,
        'equipos' : equipos,
        'usuarios': usuarios
    }
    return render(request, 'admin/index.html', data)


def contextoCompetencias(request):

    

    competencia_seleccion = competicion.objects.filter(estado=True)

    competencia_club = competicion.objects.filter(estado=True)

    data= {

        'competencia_seleccion' : competencia_seleccion,
        'competencia_club' : competencia_club
    }

    return render(request, 'competencias.html', data)

def contextoCompetenciasVivo(request):
    # Filtrar competiciones que tienen encuentros con estado_jugado='E'
    competencia_seleccion = competicion.objects.filter(encuentro__estado_jugado='E', encuentro__competicion_id__estado=True).distinct()
    competencia_club = competicion.objects.filter(encuentro__estado_jugado='E', encuentro__competicion_id__estado=True).distinct()

    data = {
        'competencia_seleccion': competencia_seleccion,
        'competencia_club': competencia_club
    }

    return render(request, 'competenciasVivo.html', data)

def contextoCompetenciasFutbol(request, nombre_competicion):
    competencia_seleccionada = competicion.objects.get(
        nombre=nombre_competicion.upper(), estado=True
    )
    fase_seleccionada = fase.objects.get(nombre="FASE DE GRUPOS")

    grupos = detalle_grupo.objects.filter(
        competicion_id=competencia_seleccionada.competicion_id,
        fase_id=fase_seleccionada.fase_id,
    ).order_by("grupo_id")

    filtro_grupos = (
        detalle_grupo.objects.filter(
            competicion_id=competencia_seleccionada.competicion_id,
            fase_id=fase_seleccionada.fase_id,
        )
        .values_list("grupo_id", flat=True)
        .distinct()
        .order_by("grupo_id")
    )

    nombre_grupos = []
    for f in filtro_grupos:
        busqueda_grupos = grupo.objects.get(grupo_id=f)
        nombre_grupos.append(busqueda_grupos)

    data = {
        "competencia_seleccionada": competencia_seleccionada,
        "grupos": grupos,
        "nombre_grupos": nombre_grupos,
    }

    return render(request, "teams.html", data)


def contextoJugador(request, alias):
    
    jugador=persona.objects.get(alias=alias.upper())

    contrato_jugador = contrato.objects.get(persona_id=jugador.persona_id, estado=True, tipo_contrato='S')

    lista_contratos_club=[]
    contratos_club= contrato.objects.filter(persona_id= jugador, tipo_contrato='C')
    for cc in contratos_club:
          lista_contratos_club.append(cc)
    
    lista_contratos_seleccion=[]
    contratos_seleccion= contrato.objects.filter(persona_id= jugador,tipo_contrato='S')
    for cs in contratos_seleccion:
          lista_contratos_seleccion.append(cs)

    data={          
        'jugador': jugador,
        'contrato': contrato_jugador,
        'contratos_club':lista_contratos_club,
        'contratos_seleccion':lista_contratos_seleccion
    }

    return render(request, 'jugador.html', data)


""" def contextoSedes(request):
    # competencia_seleccionada = competicion.objects.get(nombre=nombre_competicion.upper())   
    # encuentros = encuentro.objects.all().filter(competicion_id=competencia_seleccionada)   
    sedes_competencia=sede.objects.filter(estado='DI')
    data={
        'sedes_competencia': sedes_competencia
    }
    return render(request,'sedes.html',data) """
def obtener_sedes_por_competicion(competicion_id):
    encuentros = encuentro.objects.filter(competicion_id=competicion_id).distinct(
        "sede_id"
    )
    sedes_ids = encuentros.values_list("sede_id", flat=True)
    sedes = sede.objects.filter(sede_id__in=sedes_ids).select_related("ciudad_id")
    return sedes


def obtener_sedes_por_organizacion(organizacion_id):
    competiciones = competicion.objects.filter(organizacion_id=organizacion_id)
    encuentros = encuentro.objects.filter(competicion_id__in=competiciones).distinct('sede_id')
    sedes_ids = encuentros.values_list('sede_id', flat=True)
    sedes = sede.objects.filter(id__in=sedes_ids).select_related('ciudad_id')
    return sedes

def contextoSedes(request):
    competiciones = competicion.objects.values('nombre').annotate(min_id=Min('competicion_id')).order_by('nombre')
    competicion_id = request.GET.get("competicionId")
    sedes = (
        obtener_sedes_por_competicion(competicion_id)
        if competicion_id
        else sede.objects.all()
    )

    competicion_seleccionada = competicion.objects.filter(competicion_id=competicion_id).first()

    return render(
        request,
        "ReporteSedeCompeticion.html",
        {
            "competiciones": competiciones,
            "sedes": sedes,
            "competicion_seleccionada": competicion_seleccionada,
        },
    )

def detalle_sede(request, sede_id):
    sede_instance = get_object_or_404(sede, pk=sede_id)  # Cambia sede_id a pk
    # Aquí puedes agregar más contexto si es necesario
    return render(request, "detalle_sede.html", {"sede": sede_instance})

def contextoOrganizaciones(request):
    tipos_organizacion = obtener_tipos_organizacion()
    tipo_seleccionado = request.GET.get("tipo")

    if tipo_seleccionado:
        # Filtra las organizaciones por el tipo seleccionado
        organizaciones = organizacion.objects.filter(tipo=tipo_seleccionado)
    else:
        # Si no se selecciona un tipo, muestra todas las organizaciones
        organizaciones = organizacion.objects.all()

    return render(
        request,
        "ReporteTipoOrganizacion.html",
        {
            "tipos_organizacion": tipos_organizacion,
            "tipo_seleccionado": tipo_seleccionado,
            "organizaciones": organizaciones,
        },
    )
    
def obtener_tipos_organizacion():
    tipos = organizacion.CHOICE_TIPO
    return tipos

def lista_personas_por_tipo(request):
    tipo_personas = tipo_persona.objects.values('descripcion').annotate(min_id=models.Min('tipo_persona_id')).order_by('descripcion')
    paises = pais.objects.values('nombre').annotate(min_id=models.Min('pais_id')).order_by('nombre')
    ciudades = ciudad.objects.all()
    personas = []
    tipo_persona_seleccionada = None

    tipo_persona_id = request.GET.get("tipo_persona")
    pais_id = request.GET.get("pais")

    if tipo_persona_id:
        tipo_persona_seleccionada = tipo_persona.objects.get(pk=tipo_persona_id)
        personas = persona.objects.filter(tipo_persona_id=tipo_persona_id)

        if pais_id:
            ciudades = ciudad.objects.filter(pais_id=pais_id)
            
            personas = persona.objects.filter(ciudad_id__in=ciudades, tipo_persona_id=tipo_persona_id)
    return render(
        request,
        "Reportepersonas.html",
        {
            "tipo_personas": tipo_personas,
            "paises": paises,
            "personas": personas,
            "ciudades": ciudades,
            "tipo_persona_seleccionada": tipo_persona_seleccionada,
        },
    )
    
def lista_equipos_por_competicion_y_fase(request):
    competiciones = competicion.objects.values('nombre').annotate(min_id=Min('competicion_id')).order_by('nombre')
    fases = fase.objects.all()
    equipos = []
    competicion_seleccionada = None

    competicion_id = request.GET.get("competicion")
    fase_id = request.GET.get("fase")

    if competicion_id:
        competicion_seleccionada = competicion.objects.get(pk=competicion_id)
        if fase_id:
            detalle_grupos = detalle_grupo.objects.filter(
                competicion_id=competicion_id, fase_id=fase_id
            )
            equipos = [detalle.equipo_id for detalle in detalle_grupos]

    return render(
        request,
        "ReporteEquiposCompeticion.html",
        {
            "competiciones": competiciones,
            "fases": fases,
            "equipos": equipos,
            "competicion_seleccionada": competicion_seleccionada,
        },
    )    

# def obtener_encuentro_persona_id(encuentro_id, contrato_id):
#     try:
#         encuentro_persona_obj = encuentro_persona.objects.get(encuentro_id=encuentro_id, contrato_id=contrato_id)
#         return encuentro_persona_obj.encuentro_persona_id
#     except encuentro_persona.DoesNotExist:
#         return None


def obtener_equipo_id(encuentro_id, contrato_id):
    try:
        posicion = tabla_posicion.objects.get(encuentro_id=encuentro_id, equipo_id=contrato_id)
        return posicion.equipo_id
    except tabla_posicion.DoesNotExist:
        return None


def obtener_logo_equipo(equipo_id):
    try:
        equipo_obj = equipo.objects.get(equipo_id=equipo_id)
        equipo_logo = equipo_obj.logo.url if equipo_obj.logo else None
    except equipo.DoesNotExist:
        equipo_logo = None
    return equipo_logo

def contextoEquipo(request, nombre_equipo):
    equipos = equipo.objects.get(nombre=nombre_equipo.upper())
    tipo_persona_entrenador = tipo_persona.objects.get(descripcion="ENTRENADOR")
    persona_entrenador = persona.objects.filter(
        tipo_persona_id=tipo_persona_entrenador.tipo_persona_id
    )

    entrenadoractual = []
    for p_e in persona_entrenador:
        contratosentrenadores = contrato.objects.filter(
            persona_id=p_e.persona_id, nuevo_club=equipos.equipo_id, estado=True
        )
        for ce in contratosentrenadores:
            if ce.estado == True:
                entrenadoractual = ce

    tipo_persona_jugador = tipo_persona.objects.get(descripcion="JUGADOR")
    persona_jugador = persona.objects.filter(
        tipo_persona_id=tipo_persona_jugador.tipo_persona_id
    )

    jugadores_equipo = []
    for p_j in persona_jugador:
        contratosjugadores = contrato.objects.filter(
            persona_id=p_j.persona_id, nuevo_club=equipos.equipo_id, estado=True
        )
        for cj in contratosjugadores:
            if cj.estado == True:
                jugadores_equipo.append(cj)

    # alineacion_equipo_final = []

    # for j in jugadores:
    #     alineacionequipo = alineacion_equipo.objects.filter(contrato_id=j.contrato_id)
    #     for ae in alineacionequipo:
    #         if(ae.estado == True or ae.estado == False):
    #             alineacion_equipo_final.append(ae)
    encuentro_local_jugar = []
    encuentros_local = encuentro.objects.filter(
        equipo_local=equipos.equipo_id, estado_jugado=False
    )
    for ejl in encuentros_local:
        encuentro_local_jugar.append(ejl)

    encuentro_visita_jugar = []
    encuentros_visita = encuentro.objects.filter(
        equipo_visita=equipos.equipo_id, estado_jugado=False
    )
    for ejv in encuentros_visita:
        encuentro_visita_jugar.append(ejv)

    data = {
        "equipo": equipos,
        "entrenador": entrenadoractual,
        "jugadores_equipo": jugadores_equipo,
        "encuentro_local_jugar": encuentro_local_jugar,
        "encuentro_visita_jugar": encuentro_visita_jugar,
    }

    return render(request, "equipo.html", data)


def contextoFixtureCompetencia(request, nombre_competicion):
    
    competencia_seleccionada = competicion.objects.get(nombre=nombre_competicion.upper())   

    filtro_encuentros_competencia = encuentro.objects.filter(competicion_id=competencia_seleccionada.competicion_id)


    #total_detalles_encuentros = detalle_encuentro.objects.all()

    # for de in detalles_encuentros:
    #     for e in filtrar_encuentros_competencias:
    #         if (de.encuentro_id == e.encuentro_id):
    #             lista_detalles_encuentros_competencia.append(de)

    # for f in filtrar_encuentros_competencias:
    #     detalles_encuentros = detalle_encuentro.objects.filter(encuentro_id=f.encuentro_id)
    #     for de in detalles_encuentros:
    #         lista_detalles_encuentros_competencias.append(de)

    data={
        'competencia': competencia_seleccionada,
        'encuentros': filtro_encuentros_competencia
    }

    return render(request, 'fixtures.html', data)

def reporte_jugadores(request):
    competicion_id = request.GET.get('competicion', None)
    estadistica = request.GET.get('estadistica', 'gol')
    print(f"Competicion ID: {competicion_id}")
    print(f"Estadistica ID: {estadistica}")
    jugadores_list = []
    competiciones = competicion.objects.all()
    competicion_seleccionada = None

    tipo_evento_map = {
        'gol': 9,
        'asistencias': 19,
        'amarillas': 1,
        'rojas': 2,
    }
    tipo_evento_id = tipo_evento_map.get(estadistica, 9)
    print(f"Tipo evento ID: {tipo_evento_id}")

    if competicion_id:
        try:
            competicion_seleccionada = competicion.objects.get(pk=competicion_id)

            # Agrupar eventos por jugador y contarlos
            eventos_agrupados = evento.objects.filter(
                tipo_evento_id=tipo_evento_id,
                encuentro_id__competicion_id=competicion_id
            ).values(
                'alineacion_id1__contrato_id',
            ).annotate(
                total=Count('tipo_evento_id')
            )

            for evento_agrupado in eventos_agrupados:
                jugador_id = evento_agrupado.get('alineacion_id1__contrato_id')
                
                # Comprobar si el jugador_id es None
                if jugador_id is not None:
                    try:
                        jugador = persona.objects.get(pk=jugador_id)
                        evento_count = evento_agrupado.get('total', 0)
                        jugador.estadistica_valor = evento_count
                        contrato_jugador = contrato.objects.get(pk=jugador_id)
                        jugador.equipo_logo = contrato_jugador.nuevo_club.logo.url if contrato_jugador.nuevo_club and contrato_jugador.nuevo_club.logo else None
                        jugadores_list.append(jugador)
                        # Resto del código para procesar el jugador
                        # Puedes acceder a los campos del jugador, por ejemplo, jugador.nombre, jugador.apellido, etc.
                    except persona.DoesNotExist:
                        print(f"La persona con ID {jugador_id} no existe.")
                else:
                    print("El ID del jugador es None.")

        except competicion.DoesNotExist:
            # Manejar el caso donde la competición no existe
            pass

    return render(request, 'ReporteJugadores.html', {
        'jugadores': jugadores_list,
        'competiciones': competiciones,
        'competicion_seleccionada': competicion_seleccionada,
        'estadistica_tipo': estadistica,
    })

# def contextoListaJugadoresPorAmarillas(request,nombre_competicion):
#     competencia_seleccionada = competicion.objects.get(nombre=nombre_competicion.upper()) #FIFA WORLD CUP
#     encuentros_competencias = encuentro.objects.filter(competicion_id=competencia_seleccionada.competicion_id)

#     resulta = evento_persona.objects.filter(evento_id=1).filter(encuentro_id__in=encuentros_competencias).values('persona_id').annotate(count=Count('encuentro_evento_id')).order_by('-count') 

#     lista = [[]]

#     i = 0
#     for r in resulta:
#         li = persona.objects.get(persona_id = r.get('persona_id'))
#         lista[i].append(li)
#         lista[i].append(r.get('count'))
#         if i < len(resulta)-1:
#             lista.append([])
#         i = i + 1

#     data={
#         'jugadores_amarillas': lista
#     }

#     return render(request, 'lista_jugadores_amarillas.html', data)

# def contextoListaJugadoresPorRojas(request,nombre_competicion):
#     competencia_seleccionada = competicion.objects.get(nombre=nombre_competicion.upper()) #FIFA WORLD CUP
#     encuentros_competencias = encuentro.objects.filter(competicion_id=competencia_seleccionada.competicion_id)

#     resulta = evento_persona.objects.filter(evento_id=2).filter(encuentro_id__in=encuentros_competencias).values('persona_id').annotate(count=Count('encuentro_evento_id')).order_by('-count')
    
#     lista = [[]]

#     i = 0
#     for r in resulta:
#         li = persona.objects.get(persona_id = r.get('persona_id'))
#         lista[i].append(li)
#         lista[i].append(r.get('count'))
#         if i < len(resulta)-1:
#             lista.append([])
#         i = i + 1

#     data={
#         'jugadores_rojas': lista
#     }
#     return render(request, 'lista_jugadores_rojas.html', data)

# def contextoListaJugadoresPorAsistencias(request,nombre_competicion):
#     competencia_seleccionada = competicion.objects.get(nombre=nombre_competicion.upper()) #FIFA WORLD CUP
#     encuentros_competencias = encuentro.objects.filter(competicion_id=competencia_seleccionada.competicion_id)

#     resulta = evento_persona.objects.filter(evento_id=19).filter(encuentro_id__in=encuentros_competencias).values('persona_id').annotate(count=Count('encuentro_evento_id')).order_by('-count')  
    
#     lista = [[]]

#     i = 0
#     for r in resulta:
#         li = persona.objects.get(persona_id = r.get('persona_id'))
#         lista[i].append(li)
#         lista[i].append(r.get('count'))
#         if i < len(resulta)-1:
#             lista.append([])
#         i = i + 1

#     data={
#         'jugadores_asistencias': lista
#     }
#     return render(request, 'lista_jugadores_asistencias.html', data)

def contextoTablaPosiciones(request, nombre_competicion):
    competencia_seleccionada = competicion.objects.get(
        nombre=nombre_competicion.upper()
    )

    fase_grupos = fase.objects.get(nombre="FASE DE GRUPOS")
    listar_equipos_fase_grupos = detalle_grupo.objects.filter(
        fase_id=fase_grupos.fase_id
    ).values("equipo_id")
   
    listar_grupos_fase_grupos = (
    detalle_grupo.objects.filter(fase_id=fase_grupos.fase_id)
    .select_related('grupo')  # Optimización para evitar consultas adicionales
    .order_by("grupo_id")
    .values_list("grupo_id", flat=True)
    .distinct()
    )
    
    nombre_grupos = grupo.objects.filter(grupo_id__in=listar_grupos_fase_grupos)

    # Crear un diccionario para almacenar la información por fase y grupo
    equipos_por_grupo_info = {}

    for grupo_id in listar_grupos_fase_grupos:
        equipos_grupo = listar_equipos_fase_grupos.filter(grupo_id=grupo_id)
        equipos_tabla = (
            tabla_posicion.objects.filter(
                competicion_id=competencia_seleccionada.competicion_id,
                equipo_id__in=equipos_grupo.values_list("equipo_id", flat=True),
            )
            .values(
                "equipo_id",
                "ganado",
                "empatado",
                "perdido",
                "goles_favor",
                "goles_contra",
                "puntos",
            )
            .order_by("-puntos")
        )

        equipos_por_grupo_info[grupo_id] = []

        for i, equipo_tabla in enumerate(equipos_tabla, start=1):
            equipo_tabla_id = equipo_tabla["equipo_id"]
            equipo_modelo = equipo.objects.get(equipo_id=equipo_tabla_id)

            partidos_jugados = (
                equipo_tabla["ganado"] + equipo_tabla["empatado"] + equipo_tabla["perdido"]
            )
            diferencia_goles = equipo_tabla["goles_favor"] - equipo_tabla["goles_contra"]

            equipos_por_grupo_info[grupo_id].append({
                "posicion": i,
                "logo": equipo_modelo.logo.url,
                "nombre": equipo_modelo.nombre,
                "partidos_jugados": partidos_jugados,
                "ganados": equipo_tabla["ganado"],
                "empatados": equipo_tabla["empatado"],
                "perdidos": equipo_tabla["perdido"],
                "goles_favor": equipo_tabla["goles_favor"],
                "goles_contra": equipo_tabla["goles_contra"],
                "diferencia_goles": diferencia_goles,
                "puntos": equipo_tabla["puntos"],
            })

    data = {"equipos_por_grupo_info": equipos_por_grupo_info, "listar_grupos_fase_grupos": nombre_grupos}
    
    return render(request, "tabla-fase.html", data)


def contextoEncuentros(request, nombre_competicion):
    competencia_seleccionada = competicion.objects.get(
        nombre=nombre_competicion.upper()
    )
    encuentros_por_jugar = encuentro.objects.filter(
        competicion_id=competencia_seleccionada, estado_jugado=False
    )
    encuentros_jugados = encuentro.objects.filter(
        competicion_id=competencia_seleccionada, estado_jugado=True
    )
    data = {
        "encuentros_jugados": encuentros_jugados,
        "encuentros_por_jugar": encuentros_por_jugar,
    }
    return render(request, "encuentros_jugados.html", data)
def contextoContacto(request):
    data={

    }
    
    return render(request, 'contact.html', data)


def contextoTVvivo(request, id):
    jugar_encuentro = encuentro.objects.get(encuentro_id=id)
    equipo_a = equipo.objects.get(nombre=jugar_encuentro.equipo_local)
    equipo_b = equipo.objects.get(nombre=jugar_encuentro.equipo_visita)
    estadio = sede.objects.get(nombre=jugar_encuentro.sede_id)

    # Obtener los goles de cada equipo
    descripcion_equipo_a = descripcion_encuentro.objects.get(
        encuentro_id=id, equipo_id=equipo_a.equipo_id
    )
    descripcion_equipo_b = descripcion_encuentro.objects.get(
        encuentro_id=id, equipo_id=equipo_b.equipo_id
    )

    data = {
        'jugar_encuentro': jugar_encuentro,
        'equipo_a': equipo_a,
        'equipo_b': equipo_b,
        'estadio': estadio,
        'goles_equipo_a': descripcion_equipo_a.goles,
        'goles_equipo_b': descripcion_equipo_b.goles,
    }
    
    return render(request, 'tvVivo.html', data)


def contextoTVhome(request, idCompeticion):
    # Obtener encuentros en juego
    encuentrosEnJuego = encuentro.objects.filter(estado_jugado='E', competicion_id=idCompeticion)
    encuentrosJugados = encuentro.objects.filter(estado_jugado='F', competicion_id=idCompeticion)

    # Crear el diccionario de datos
    data = {'encuentrosE': [],'encuentrosJ': []}
    print(encuentrosEnJuego)
    # Iterar sobre los encuentros en juego para obtener los goles
    for encuentroEnJuego in encuentrosEnJuego:
        # Obtener los goles locales y visitantes directamente
        golesLocal = descripcion_encuentro.objects.filter(tipo_equipo='LOCAL', encuentro_id=encuentroEnJuego.encuentro_id).values_list('goles', flat=True).first()
        golesVisita = descripcion_encuentro.objects.filter(tipo_equipo='VISITA', encuentro_id=encuentroEnJuego.encuentro_id).values_list('goles', flat=True).first()

        # Agregar el encuentro y sus goles al diccionario
        data['encuentrosE'].append({
            'encuentro': encuentroEnJuego,
            'golesLocal': golesLocal,
            'golesVisita': golesVisita,
        })
        
            # Crear el diccionario de datos

    # Iterar sobre los encuentros en juego para obtener los goles
    for encuentroJugado in encuentrosJugados:
        # Obtener los goles locales y visitantes directamente
        golesLocal = descripcion_encuentro.objects.filter(tipo_equipo='LOCAL', encuentro_id=encuentroJugado.encuentro_id).values_list('goles', flat=True).first()
        golesVisita = descripcion_encuentro.objects.filter(tipo_equipo='VISITA', encuentro_id=encuentroJugado.encuentro_id).values_list('goles', flat=True).first()

        # Agregar el encuentro y sus goles al diccionario
        data['encuentrosJ'].append({
            'encuentro': encuentroJugado,
            'golesLocal': golesLocal,
            'golesVisita': golesVisita,
        })

    # Obtener información de la competición
    competiciones = competicion.objects.get(competicion_id=idCompeticion)

    # Obtener encuentros por jugar
    encuentrosPorJugar = encuentro.objects.filter(estado_jugado='N', competicion_id=idCompeticion)
    
    # Obtener encuentros jugados

    # Agregar al diccionario de datos
    data['encuentrosN'] = encuentrosPorJugar

    data['competiciones'] = competiciones

    return render(request, 'tvHome.html', data)


def contextoTVhomeVivo(request, idCompeticion):
    # Obtener encuentros en juego
    encuentrosEnJuego = encuentro.objects.filter(estado_jugado='E', competicion_id=idCompeticion)

    # Crear el diccionario de datos
    data = {'encuentrosE': []}

    # Iterar sobre los encuentros en juego para obtener los goles
    for encuentroEnJuego in encuentrosEnJuego:
        # Obtener los goles locales y visitantes directamente
        golesLocal = descripcion_encuentro.objects.filter(tipo_equipo='LOCAL', encuentro_id=encuentroEnJuego.encuentro_id).values_list('goles', flat=True).first()
        golesVisita = descripcion_encuentro.objects.filter(tipo_equipo='VISITA', encuentro_id=encuentroEnJuego.encuentro_id).values_list('goles', flat=True).first()

        # Agregar el encuentro y sus goles al diccionario
        data['encuentrosE'].append({
            'encuentro': encuentroEnJuego,
            'golesLocal': golesLocal,
            'golesVisita': golesVisita,
        })

    # Obtener información de la competición
    competiciones = competicion.objects.get(competicion_id=idCompeticion)

    # Obtener encuentros por jugar
    encuentrosPorJugar = encuentro.objects.filter(estado_jugado='N', competicion_id=idCompeticion)

    # Agregar al diccionario de datos
    data['encuentrosN'] = encuentrosPorJugar
    data['competiciones'] = competiciones

    return render(request, 'tvHomeVivo.html', data)


def contextoTVhomeEncuentro(request,id):
    jugar_encuentro=encuentro.objects.get(encuentro_id=id)
    equipo_a=equipo.objects.get(nombre=jugar_encuentro.equipo_local)
    equipo_b=equipo.objects.get(nombre=jugar_encuentro.equipo_visita)
    descripcion_local = descripcion_encuentro.objects.get(equipo=equipo_a.equipo_id, encuentro_id=id)
    descripcion_visita = descripcion_encuentro.objects.get(equipo=equipo_b.equipo_id, encuentro_id=id)
    eventos_local = evento.objects.filter(alineacion_id1__contrato_id__nuevo_club=equipo_a, encuentro_id=id)
    eventos_visita = evento.objects.filter(alineacion_id1__contrato_id__nuevo_club=equipo_b, encuentro_id=id)
    eventos_todos = evento.objects.filter( encuentro_id=id)
    ronda_penal = False
        
    # Ordena los eventos por tiempo en orden ascendente
    eventos_todos = sorted(eventos_todos, key=attrgetter('tiempo'))
    estado_gol = False
    estado_tarjeta = False
    jugadores_dict = {}
    jugadores_penales = []
    # Supongamos que tienes una lista llamada 'eventos' con la información de los eventos
    conteo_gol_local = sum(1 for evento in eventos_local if evento.tipo_evento_id.nombre == 'GOL RONDA PENAL' and evento.evento_equipo == True)
    conteo_gol_visita = sum(1 for evento in eventos_visita if evento.tipo_evento_id.nombre == 'GOL RONDA PENAL' and evento.evento_equipo== False)
    conteo_gol_visita_simultaneo = 0
    conteo_gol_local_simultaneo = 0
    for i in eventos_todos:
        if i.tipo_evento_id.nombre == 'GOL' or i.tipo_evento_id.nombre == 'GOL PENAL':
            estado_gol = True
            jugador_alias = i.alineacion_id1.contrato_id.persona.alias

            # Determinar si el evento es del equipo LOCAL o VISITA
            equipo_evento = 'LOCAL' if i.evento_equipo == True else 'VISITA'

            if i.tipo_evento_id.nombre == 'GOL PENAL':
                if i.tiempo_extra:
                    tiempo = str(i.tiempo) + "+" + str(i.tiempo_extra) + "' (P)"
                else:
                    tiempo = str(i.tiempo) + "' (P)"

            else:
                if i.tiempo_extra:
                    tiempo = str(i.tiempo) + "+" + str(i.tiempo_extra) + "'"
                else:
                    tiempo = str(i.tiempo) + "'"

            if jugador_alias in jugadores_dict:
                jugadores_dict[jugador_alias]['tiempos'].append(tiempo)
            else:
                jugadores_dict[jugador_alias] = {'tiempos': [tiempo], 'equipo': equipo_evento}

        if i.tipo_evento_id.nombre == 'TARJETA ROJA':
            estado_tarjeta = True
        if i.tipo_evento_id.nombre == 'RONDA DE PENALES':
            ronda_penal = True
        if i.tipo_evento_id.nombre == 'GOL RONDA PENAL' or i.tipo_evento_id.nombre == 'NO GOL RONDA PENAL':
            jugador_penal = i.alineacion_id1.contrato_id.persona.alias
            equipo_evento = 'LOCAL' if i.evento_equipo == True else 'VISITA'
            if i.tipo_evento_id.nombre == 'GOL RONDA PENAL' and i.evento_equipo == True:
                conteo_gol_local_simultaneo = conteo_gol_local_simultaneo + 1
            elif i.tipo_evento_id.nombre == 'GOL RONDA PENAL' and i.evento_equipo == False:
                conteo_gol_visita_simultaneo = conteo_gol_visita_simultaneo + 1

            # Verificar si el equipo es 'LOCAL' y agregar el jugador penal correspondiente
            if equipo_evento == 'LOCAL':
                if len(jugadores_penales) == 0 or jugadores_penales[-1]['local'] is not '':
                    jugadores_penales.append({'local': jugador_penal, 'visita': '', 'gol_local': i.tipo_evento_id.nombre, 'gol_visita': '','goles_local':conteo_gol_local_simultaneo, 'goles_visita':conteo_gol_visita_simultaneo,'goles_local_primero':conteo_gol_local_simultaneo, 'goles_visita_primero':conteo_gol_visita_simultaneo})
                else:
                    jugadores_penales[-1]['local'] = jugador_penal
                    jugadores_penales[-1]['gol_local'] = i.tipo_evento_id.nombre
                    jugadores_penales[-1]['goles_local'] = conteo_gol_local_simultaneo
            # Verificar si el equipo es 'VISITA' y agregar el jugador penal correspondiente
            else:
                if len(jugadores_penales) == 0 or jugadores_penales[-1]['visita'] is not '':
                    jugadores_penales.append({'local': '', 'visita': jugador_penal, 'gol_local': '', 'gol_visita': i.tipo_evento_id.nombre, 'goles_local':conteo_gol_local_simultaneo, 'goles_visita':conteo_gol_visita_simultaneo,'goles_local_primero':conteo_gol_local_simultaneo, 'goles_visita_primero':conteo_gol_visita_simultaneo})
                else:
                    jugadores_penales[-1]['visita'] = jugador_penal
                    jugadores_penales[-1]['gol_visita'] = i.tipo_evento_id.nombre
                    jugadores_penales[-1]['goles_visita'] = conteo_gol_visita_simultaneo

    list_jugadores = [{'jugador': jugador, 'tiempos': ', '.join(map(str, data['tiempos'])), 'equipo': data['equipo']} for jugador, data in jugadores_dict.items()]

    for i in eventos_visita:
        print('evento',i.tipo_evento_id.nombre)
    print(list_jugadores)
    data={
        'conteo_gol_visita':conteo_gol_visita,
        'conteo_gol_local':conteo_gol_local,
        'jugadores_penales':jugadores_penales,
          'ronda_penal':ronda_penal,
          'list_jugadores':list_jugadores,
          'equipo_local': equipo_a,
          'equipo_visita': equipo_b,
          'encuentro' : jugar_encuentro,
          'descripcion_local':descripcion_local,
          'descripcion_visita':descripcion_visita,
          'eventos_local':eventos_local,
          'eventos_visita':eventos_visita,
          'eventos_todos': eventos_todos,
          'estado_gol':estado_gol,
          'estado_tarjeta':estado_tarjeta,
    }
    return render(request, 'tvHomeEncuentro.html', data)

def contextoTv(request,id):
    jugar_encuentro=encuentro.objects.get(encuentro_id=id)
    equipo_a=equipo.objects.get(nombre=jugar_encuentro.equipo_local)
    equipo_b=equipo.objects.get(nombre=jugar_encuentro.equipo_visita)
    estadio=sede.objects.get(nombre=jugar_encuentro.sede_id)
    encuentro_goles=evento.objects.filter(encuentro_id=jugar_encuentro.encuentro_id,evento_id=9)
    encuentro_tarjetasA=evento.objects.filter(encuentro_id=jugar_encuentro.encuentro_id,evento_id=1)
    encuentro_tarjetasR=evento.objects.filter(encuentro_id=jugar_encuentro.encuentro_id,evento_id=2)
    
    terna_encuentro=detalle_terna.objects.get(terna_arbitral_id=jugar_encuentro.terna_arbitral_id_id)    
    detalle_terna_encuentro=detalle_terna.objects.filter(terna_arbitral_id=terna_encuentro.terna_arbitral_id).values('arbitro_id')
    arbitros=persona.objects.filter(arbitro_id__in=detalle_terna_encuentro)


    alineacion_encuentro_a=encuentro.objects.filter(encuentro_id=id).values('alineacion_local')
    alineacion_a=alineacion.objects.filter(alineacion_id__in=alineacion_encuentro_a, estado=True).values('alineacion_id')
    detalle_alineacion_a=alineacion.objects.filter(alineacion_id__in=alineacion_a,equipo_id=equipo_a.equipo_id).values('contrato_id')
    contrato_alineacion_a=contrato.objects.filter(contrato_id__in=detalle_alineacion_a).values('persona_id')
    personas_alineacion_a=persona.objects.filter(persona_id__in=contrato_alineacion_a)

    alineacion_encuentro_b=encuentro.objects.filter(encuentro_id=id).values('alineacion_visita')
    alineacion_b=alineacion.objects.filter(alineacion_id__in=alineacion_encuentro_b, estado=True).values('alineacion_id')    
    detalle_alineacion_b=alineacion.objects.filter(alineacion_id__in=alineacion_b,equipo_id=equipo_b.equipo_id).values('contrato_id')
    contrato_alineacion_b=contrato.objects.filter(contrato_id__in=detalle_alineacion_b).values('persona_id')
    personas_alineacion_b=persona.objects.filter(persona_id__in=contrato_alineacion_b)
    

    data={
        'jugar_encuentro':jugar_encuentro,
        'equipo_a':equipo_a,
        'equipo_b':equipo_b,
        'estadio':estadio,
        'encuentro_goles':encuentro_goles,
        'encuentro_tarjetasA': encuentro_tarjetasA,
        'encuentro_tarjetasR': encuentro_tarjetasR,
        'arbitros':arbitros,
        'personas_alineacion_a':personas_alineacion_a,
        'personas_alineacion_b':personas_alineacion_b,
    }
    
    return render(request, 'single-result.html', data)
    
def index(request):
    data={
    }
    return render(request, 'index.html', data)

def cambiar_estado_encuentro_E(request):
    if request.method == 'POST':
        # Obtén el ID del encuentro y realiza el cambio de estado
        encuentro_id = request.POST.get('encuentro_id')
        try:
            encuentro_obj = encuentro.objects.get(encuentro_id=encuentro_id)
            encuentro_obj.estado_jugado = 'E'
            encuentro_obj.save()
            return JsonResponse({'success': True})
        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'error': 'No se encontró el encuentro'})
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'})
def cambiar_estado_encuentro_F(request):
    if request.method == 'POST':
        # Obtén el ID del encuentro y realiza el cambio de estado
        encuentro_id = request.POST.get('encuentro_id')
        # Realiza aquí el cambio de estado en tu modelo Encuentro
        # Por ejemplo:
        encuentro_obj = encuentro.objects.get(encuentro_id=encuentro_id)
        encuentro_obj.estado_jugado = 'F'
        encuentro_obj.save() 

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'})



def mostrarEncuentrosEvento(request):
    competicion_id = request.GET.get('competicion')
    fase_id = request.GET.get('fase')
    grupo_id = request.GET.get('grupo') 

    if competicion_id == 'todas' and fase_id == 'todas':
        encuentros = encuentro.objects.filter(estado_jugado__in=['N', 'E'],)
        encuentrosParaFiltro = encuentro.objects.all()
    elif competicion_id != 'todas' and fase_id == 'todas':
        encuentros = encuentro.objects.filter(estado_jugado__in=['N', 'E'], competicion_id=competicion_id)
        encuentrosParaFiltro = encuentro.objects.filter(competicion_id=competicion_id)

    elif competicion_id == 'todas' and fase_id != 'todas':
        encuentros = encuentro.objects.filter(estado_jugado__in=['N', 'E'], fase_id=fase_id)
        encuentrosParaFiltro = encuentro.objects.all()
        if fase_id == '1' and grupo_id != 'todas':
            encuentros = encuentros.filter(grupo_id=grupo_id)
    else:
        encuentros = encuentro.objects.filter(estado_jugado__in=['N', 'E'], competicion_id=competicion_id, fase_id=fase_id)
        encuentrosParaFiltro = encuentro.objects.filter(competicion_id=competicion_id)
       
        if fase_id == '1' and grupo_id != 'todas':
            encuentros = encuentros.filter(grupo_id=grupo_id)

    fases = fase.objects.filter(fase_id__in=encuentrosParaFiltro.values('fase_id')).distinct()
    grupos = grupo.objects.filter(grupo_id__in=encuentrosParaFiltro.values('grupo_id')).distinct().order_by('grupo_id')
    print(fase_id)
    print(competicion_id)
    print(grupos)
    print(encuentros)

    # Obtén las opciones para los combobox de filtro
    competiciones = competicion.objects.all()
    if request.method == 'POST':
        idEncuentro = request.POST.get('idEncuentro')
        print("El encuentro id es: ",idEncuentro)
        return redirect('mostrar_eventos_generales', idEncuentro=idEncuentro)         
        
    return render(
        request,
        'moduloTV/listaEncuentros.html',
        {
            'encuentros': encuentros,
            'fases':fases,
            'competiciones': competiciones,
            'competicion_id':competicion_id,
            'fase_id':fase_id,
            'grupos':grupos,
            'grupo_id':grupo_id,
        }
    )



def mostrarEventos(request, idEncuentro):
    # Manejo de la solicitud POST
    if request.method == 'POST':
        eventos_seleccionados = request.POST.getlist('idEvento')
        eventos_para_actualizar = evento.objects.filter(evento_id__in=eventos_seleccionados)
        
        # Aquí asumo que 'guardar_eventos_temporales' es una función que necesitas ejecutar.
        guardar_eventos_temporales(eventos_para_actualizar)

        for evento_seleccionado in eventos_para_actualizar:
            print(f"Eventos seleccionado: {evento_seleccionado}")
            # Suponiendo que quieras cambiar el estado_evento a False
            evento_seleccionado.estado_evento = False
            evento_seleccionado.save()

        # Redirige a la misma página para evitar reenvíos de formulario
        return redirect('mostrar_evento', idEncuentro=idEncuentro)

    # Manejo de la solicitud GET
    tipo_filtro = request.GET.get('filtro', 'en_juego')
    nombres_eventos_generales = ["CRONOMETRO", "PARTIDO SUSPENDIDO"]

    if tipo_filtro == 'generales':
        eventos = evento.objects.filter(encuentro_id=idEncuentro, estado_evento=True, tipo_evento_id__nombre__in=nombres_eventos_generales)
        redirect('moduloTV/GeneralesTV.html',eventos)
    elif tipo_filtro == 'en_juego':
        eventos = evento.objects.filter(encuentro_id=idEncuentro, estado_evento=True).exclude(tipo_evento_id__nombre__in=nombres_eventos_generales)
        
    else:
        eventos = evento.objects.none()

    return render(request, 'moduloTV/evento.html', {'eventos': eventos, 'tipo_filtro': tipo_filtro})



###
# views.py
# ...

def base_evento_view(request, idEncuentro, template_name, filtro_default):

    if request.method == 'POST'and filtro_default=='en_juego':
        eventos_seleccionados = request.POST.getlist('idEvento')
        eventos_para_actualizar = evento.objects.filter(evento_id__in=eventos_seleccionados)
        tiempo = request.POST.get('tiempo')
        print(tiempo)
        # Lógica específica para cada vista hija
        guardar_eventos_temporales(eventos_para_actualizar,tiempo)

        for evento_seleccionado in eventos_para_actualizar:
            evento_seleccionado.estado_evento = False
            evento_seleccionado.save()


    tipo_filtro = request.GET.get('filtro', filtro_default)
    nombres_eventos_generales = ["CRONOMETRO", "PARTIDO SUSPENDIDO"]
    equipo_local=''
    equipo_visita=''
    alineaciones_local = ''
    alineaciones_visita=''
    formacion_local=''
    formacion_visita=''

    if tipo_filtro == 'generales':

        eventos = evento.objects.none()
        encuentro_obj = encuentro.objects.filter(encuentro_id=idEncuentro).first()

        equipo_local = descripcion_encuentro.objects.filter( 
                encuentro_id=idEncuentro,
                equipo_id__in=[encuentro_obj.equipo_local, encuentro_obj.equipo_visita],tipo_equipo__in=['L','Local','LOCAL']
            ).first()
        equipo_visita = descripcion_encuentro.objects.filter( 
                encuentro_id=idEncuentro,
                equipo_id__in=[encuentro_obj.equipo_visita, encuentro_obj.equipo_visita],tipo_equipo__in=['V','Visita','VISITA']
            ).first()
        alineaciones_local = alineacion.objects.filter(descripcion_encuentro_id=equipo_local.descripcion_encuentro_id).order_by('-estado', 'dorsal')
        alineaciones_visita = alineacion.objects.filter(descripcion_encuentro_id=equipo_visita.descripcion_encuentro_id).order_by('-estado', 'dorsal')
        formacion_local =  alineacion.objects.filter(descripcion_encuentro_id=equipo_local.descripcion_encuentro_id).first()
        formacion_visita =  alineacion.objects.filter(descripcion_encuentro_id=equipo_visita.descripcion_encuentro_id).first()
        print('Alineacion local',equipo_local)
        print('Alineacion visita',formacion_visita.formacion)

    elif tipo_filtro == 'en_juego':
        eventos = evento.objects.filter(encuentro_id=idEncuentro).exclude(tipo_evento_id__nombre__in=nombres_eventos_generales).reverse()
        encuentro_obj = encuentro.objects.filter(encuentro_id=idEncuentro).first()

        equipo_local = descripcion_encuentro.objects.filter( 
                encuentro_id=idEncuentro,
                equipo_id__in=[encuentro_obj.equipo_local, encuentro_obj.equipo_visita],tipo_equipo__in=['L','Local','LOCAL']
            ).first()
        equipo_visita = descripcion_encuentro.objects.filter( 
                encuentro_id=idEncuentro,
                equipo_id__in=[encuentro_obj.equipo_visita, encuentro_obj.equipo_visita],tipo_equipo__in=['V','Visita','VISITA']
            ).first()
    else:
        print('Template name evento:', template_name)
        eventos = evento.objects.none()

    return render(request, template_name, {'eventos': eventos, 'tipo_filtro': tipo_filtro,'idEncuentro': idEncuentro, 'equipo_local':equipo_local,'equipo_visita':equipo_visita,'alineacion_local':alineaciones_local,'alineacion_visita':alineaciones_visita, 'formacion_local':formacion_local, 'formacion_visita':formacion_visita})

def mostrarEvento(request, idEncuentro):
    return base_evento_view(request, idEncuentro, 'moduloTV/evento.html',filtro_default='en_juego')

def mostrarEventosGenerales(request, idEncuentro):
    banners = []
    html_dinamico = request.POST.getlist('miTextarea')
    alineaciones_existen = alineacion.objects.filter(descripcion_encuentro_id__encuentro_id=idEncuentro).exists()

    if not alineaciones_existen:
            # Si no hay alineaciones registradas, muestra un mensaje de advertencia
        messages.success(
            request, 'El ecuentro no tiene alineaciones registradas')
        return redirect(f"/admintv/encuentros?competicion=todas&fase=todas")

    print(html_dinamico)
    if request.method == 'POST':
        print("POST request recibido")
        print(request.POST)  # Imprime los datos POST
        html_dinamico = request.POST.getlist('miTextarea')
        print("El html dinamico es",html_dinamico)
        tiempo = request.POST.get('tiempo')

        if not tiempo:
            tiempo=10
            # Verificar si hay alineaciones registradas para el encuentro

        print("El tiempo es",tiempo)
        html_dinamico = {'html': request.POST.get('miTextarea'),'tiempo':tiempo}
        # print(html_dinamico)
        banners.append(html_dinamico)
        contenido = json.dumps({'banners': banners})
        default_storage.save('eventos_temporales.json', ContentFile(contenido))
            
    
    return base_evento_view(request, idEncuentro, 'moduloTV/GeneralesTv.html', filtro_default='generales')





#####





def guardar_eventos_temporales(eventos,tiempo):
    default_storage.delete('eventos_temporales.json')
    
    banners = []

    for evento in eventos:
        if evento.tipo_evento_id.nombre == 'CAMBIO DE JUGADOR':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7); margin-top: 43%; text-align: justify; padding-left: 20%;"><div style="display: flex; align-items: center;"><img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 15%; position: relative; margin-right: 10px;">'
                        f'<div style="flex-grow: 1;">{evento.tipo_evento_id.nombre}: <br><img src="/static/images/evento/entra.png" alt="" style="width: 5%;"><span> {evento.alineacion_id2} </span><br> <img src="/static/images/evento/sale.png" alt="" style="width: 5%;"> <span> {evento.alineacion_id1} </span></div></div></div>',
                'tiempo': tiempo
            }

        elif evento.tipo_evento_id.nombre == 'CORNER':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento_id.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("imagenes/evento/corner.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'POSICION':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento_id.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("imagenes/evento/posicion.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'TIRO LIBRE DIRECTO':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento_id.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;padding-left: -100px;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("imagenes/evento/tiro_libre.png")}" alt="" style="margin-top:0px; width: 6%"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'TIRO LIBRE INDIRECTO':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento_id.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("imagenes/evento/tiro_libre.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'PENALTY':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento_id.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("imagenes/evento/penalty.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'LESIÓN':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento_id.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("imagenes/evento/lesion.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'ATAJADAS':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento_id.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("imagenes/evento/atajada.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'REMATE':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento_id.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("images/evento/remate.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'REMATE AL ARCO':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="margin-top:0px; width: 6%"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("img/tarjeta_roja.png")}" alt="" style="margin-top:0px; width: 6%"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'REMATE AL DESVIADO':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("img/tarjeta_roja.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'SAQUE DE BANDA':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("img/tarjeta_roja.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'SAQUE DE META':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("img/tarjeta_roja.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'ASISTENCIA':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("img/tarjeta_roja.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'ATAQUE':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("img/tarjeta_roja.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'ATAQUE PELIGROSO':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("img/tarjeta_roja.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'DISPARO AL PALO':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("img/tarjeta_roja.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'RECUPERACION DE BALON':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("img/tarjeta_roja.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'INTERSECCION':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("img/tarjeta_roja.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'DESPEJE':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("img/tarjeta_roja.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'TEST':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("img/tarjeta_roja.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'ESTADISTICAS FINALES':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7); margin-top: 50%;">{evento.tipo_evento_id.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("img/tarjeta_roja.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        # elif evento.tipo_evento_id.nombre == 'CARA A CARA':
        #     banner = {
        #         'html': f'<div class="banner-container">{evento.motivo}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="margin-top:0px; width: 6%"> <span style="padding-right: 20px;"> {evento.alineacion_id1} </span><img src="{static("img/tarjeta_roja.png")}" alt="" style="margin-top:0px; width: 6%"></div>','tiempo':tiempo
        #     }
        elif evento.tipo_evento_id.nombre == 'TARJETA ROJA':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7); margin-top: 50%;"  >{evento.tipo_evento_id.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("images/evento/tarjeta_roja.png")}" alt="" style="width: 7%;margin-top: -5%;"></div>','tiempo':tiempo
            }

        elif evento.tipo_evento_id.nombre == 'TARJETA AMARILLA':
             banner = {
               'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7); margin-top: 50%;" >{evento.tipo_evento_id.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style=" width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("images/evento/tarjeta_amarilla.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }

        elif evento.tipo_evento_id.nombre == 'GOL':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%; ">{evento.tipo_evento_id.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="width: 13%;margin-top: -5%;"> <span style="padding-right: 5px;padding-left: 5px;"> {evento.alineacion_id1} </span><img src="{static("images/evento/gol.png")}" alt="" style="width: 13%;margin-top: -5%;"></div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.descripcion == 'TIEMPO EXTRA':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);"> +{evento.cantidad} </div>','tiempo':tiempo
            }
        elif evento.tipo_evento_id.nombre == 'PARTIDO SUSPENDIDO':
            banner = {
            'html': f'<div class="banner-container" style="background-color: red; color: white">PARTIDO SUSPENDIDO</div>'
            }
        elif evento.tipo_evento_id.nombre == 'CRONOMETRO':
            banner = {
            'html': f'<div class="banners-container" style=" position: absolute;top: 230px; right: 1100px;background-color: rgb(210, 210, 210);color: black;text-align: center;height: 30px;width: 280px;font-size: 16px;border-radius: 5px;z-index: 1;"><span id="cronometro" style="background-color: rgb(210, 210, 210); color: black;">00:00</span><img src="{evento.encuentro_id.equipo_local.sede_id.ciudad_id.pais_id.logo_bandera.url}" alt=""style="margin-top:0px; width: 13%"><span> {evento.encuentro_id.equipo_local.siglas} </span><span id="marcador-local">0</span> - <spanid="marcador-visitante">0</span></span><span> {evento.encuentro_id.equipo_visita.siglas} </span><img src="{evento.encuentro_id.equipo_visita.sede_id.ciudad_id.pais_id.logo_bandera.url}" alt=""style="margin-top:0px; width: 13%"></div>','tiempo':tiempo
            };tiempo
        elif evento.tipo_evento_id.nombre == 'FALTA':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);  margin-top: 50%;">{evento.tipo_evento.nombre}: <br> <img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="margin-top:0px; width: 6%"> <span style="padding-right: 20px;"> {evento.alineacion_id1} </span><img src="{static("img/falta.png")}" alt="" style="margin-top:0px; width: 6%"></div>','tiempo':tiempo
            };tiempo
        elif evento.tipo_evento_id.nombre == 'ENTRENADOR':
            banner = {
                'html': f'<div class="banner-container" style="background-color: rgba(0, 0, 0, 0.7);"><img src="/static/images/{evento.alineacion_id1.descripcion_encuentro_id.equipo.logo}" alt="" style="margin-top:0px; width: 6%"> <span style="padding-right: 20px;"> {evento.alineacion_id1} </span><img src="{static("img/entrenador.png")}" alt="" style="margin-top:0px; width: 6%"></div>','tiempo':tiempo
            };tiempo
     

        else:    
            banner = {
                'html': f'<div class="banner-container">{evento.tipo_evento_id} </div>','tiempo':tiempo
            }
        banners.append(banner)


    print('esto es',evento.tipo_evento_id.descripcion)

    



    contenido = json.dumps({'banners': banners})

    default_storage.save('eventos_temporales.json', ContentFile(contenido))






def obtener_eventos_ajax(request):
    eventos_temporales = []

    try:
        with default_storage.open('eventos_temporales.json', 'r') as archivo_json:
            eventos_dict = json.load(archivo_json)
            eventos_temporales = eventos_dict['banners']
    except FileNotFoundError:
        pass

    return JsonResponse({'banners': eventos_temporales})


def limpiar_eventos_temporales(request):
    try:
        # Intenta eliminar el archivo temporal 'eventos_temporales.json'
        default_storage.delete('eventos_temporales.json')
        return JsonResponse({'message': 'Archivo temporal eliminado correctamente'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

### API DE TARJETAS
def infracciones(request,tipo, idContrato):
    veces = alineacion.objects.filter(contrato_id=idContrato)

    resultado = 0

    # TARJETAS AMARILLAS
    if tipo == 1:
        resultado = evento.objects.filter(alineacion_id1__in=[vez.alineacion_id for vez in veces], tipo_evento_id=1).count()

    # TARJETAS ROJAS
    elif tipo == 2:
        resultado = evento.objects.filter(alineacion_id1__in=[vez.alineacion_id for vez in veces], tipo_evento_id=2).count()

    # GOLES TOTALES
    elif tipo == 3:
        resultado = evento.objects.filter(alineacion_id1__in=[vez.alineacion_id for vez in veces], tipo_evento_id=9).count()

    return JsonResponse({'resultado': resultado})


####
#Esto se podria eliminar       
def contextotablaorganizacion(request):
    
    competiciones = competicion.objects.all()

    data ={
        'competiciones' : competiciones
    }

    return render (request,'organizacion.html', data)
#


def contextotablaorganizacionindi(request, orga_id):
    print(orga_id)
    competiciones = competicion.objects.filter(organizacion_id=orga_id)
    data ={
        'competiciones' : competiciones
    }

    return render (request,'organizacion.html', data)

def apicompetenciasequipo(request,nombre_competicion):
    try:
        # Busca la competición por nombre
        #competencia_seleccionada = competicion.objects.get(nombre=nombre_competicion.upper(), estado=True)
        competencia_seleccionada = competicion.objects.get(nombre=nombre_competicion.upper())

        # Obtiene las posiciones de tabla para la competición seleccionada
        posiciones = tabla_posicion.objects.filter(competicion_id=competencia_seleccionada)

        # Extrae los equipos relacionados con las posiciones de tabla
        equipos_de_la_competicion = [posicion.equipo_id for posicion in posiciones]

        # Construye una lista de diccionarios con los detalles de los equipos
        equipos_data = [{'nombre': equipo.nombre, 'logo': equipo.logo.url, 'siglas':  equipo.siglas} for equipo in equipos_de_la_competicion]

        data =  {'equipos': equipos_data}

    except FileNotFoundError:
        data = {'error': 'Error al mostrar la data de Competiciones'}

    return JsonResponse(data)

@csrf_exempt
def actualizar_cronometro(request):
    try:
        data = json.loads(request.body)
        accion = data.get('accion')
        tiempo = data.get('tiempo')

        # Realiza las acciones necesarias con 'accion' y 'tiempo'
        # Puedes almacenar la información en la base de datos, por ejemplo.
        response_data = {'accion': accion, 'tiempo': tiempo}
        contenido = json.dumps(response_data)
        nombre_archivo = 'tempo_crono.json'
        
        # Elimina el archivo si ya existe
        if default_storage.exists(nombre_archivo):
            default_storage.delete(nombre_archivo)
        
        # Guarda el contenido en el mismo archivo
        default_storage.save(nombre_archivo, ContentFile(contenido))  
          
        return JsonResponse(response_data)
    
    except Exception as e:
        response_data = {'status': 'error', 'message': str(e)}
        return JsonResponse(response_data, status=500)
    



    
def obtener_hora_actual(request):
    tempo_crono = []

    try:
        with default_storage.open('tempo_crono.json', 'r') as archivo_json:
            eventos_dict = json.load(archivo_json)
            accion = eventos_dict['accion']
            tiempo = eventos_dict['tiempo']
    except FileNotFoundError:
        pass

    return JsonResponse({'accion': accion, 'tiempo':tiempo}) 