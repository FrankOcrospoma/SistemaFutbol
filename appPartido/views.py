from django.http import JsonResponse
from django.views import View
from .models import *
from appCompeticion.models import *
from appEquipo.models import *
from appContrato.models import *
from django.shortcuts import render, get_object_or_404,  redirect
from django.contrib import messages
from datetime import datetime


class ObtenerEncuentrosView(View):
    def get(self, request, *args, **kwargs):
        competicion_id = request.GET.get('competicion_id')
        encuentros = encuentro.objects.filter(competicion_id=competicion_id)
        data = {encuentro.encuentro_id: str(
            encuentro) for encuentro in encuentros}
        return JsonResponse(data)


class ObtenerAlineacionesView(View):
    def get(self, request, *args, **kwargs):
        encuentro_id = request.GET.get('encuentro_id')
        tipo_evento_id = request.GET.get('tipo_evento_id')

        encuentro_obj = encuentro.objects.get(encuentro_id=encuentro_id)

        # Obtener todos los objetos que cumplen con la condición
        descripcionEncuentroLocal_objs = descripcion_encuentro.objects.filter(
            equipo=encuentro_obj.equipo_local)
        descripcionEncuentroVisita_objs = descripcion_encuentro.objects.filter(
            equipo=encuentro_obj.equipo_visita)

        # Obtener alineaciones asociadas a los objetos obtenidos
        alineacionLocal_objs = alineacion.objects.filter(
            descripcion_encuentro_id__in=descripcionEncuentroLocal_objs)
        alineacionVisita_objs = alineacion.objects.filter(
            descripcion_encuentro_id__in=descripcionEncuentroVisita_objs)

        if tipo_evento_id == '3':
            data = {
                'alineacion1': [{'id': str(alineacion.alineacion_id), 'jugador': str(alineacion.contrato_id)} for alineacion in alineacionLocal_objs],
                'alineacion2': [{'id': str(alineacion.alineacion_id), 'jugador': str(alineacion.contrato_id)} for alineacion in alineacionLocal_objs],
            }
        elif tipo_evento_id == '37':
            data = {
                'alineacion1': [{'id': str(alineacion.alineacion_id), 'jugador': str(alineacion.contrato_id)} for alineacion in alineacionVisita_objs],
                'alineacion2': [{'id': str(alineacion.alineacion_id), 'jugador': str(alineacion.contrato_id)} for alineacion in alineacionVisita_objs],
            }
        else:
            data = {
                'alineacion1': [{'id': str(alineacion.alineacion_id), 'jugador': str(alineacion.contrato_id)} for alineacion in alineacionLocal_objs],
                'alineacion2': [{'id': str(alineacion.alineacion_id), 'jugador': str(alineacion.contrato_id)} for alineacion in alineacionVisita_objs],
            }

        return JsonResponse(data)

def mostrarEncuentros(request):
    tipo = request.GET.get('tipo')
    competicion_id = request.GET.get('competicion')
    fase_id = request.GET.get('fase')
    grupo_id = request.GET.get('grupo') 

    if tipo == 'alineaciones' or tipo == 'terna_arbitral':
        estado_filter = 'N'
    elif tipo == 'eventos' or tipo == 'estadisticas':
        estado_filter = 'E'
    else:
        estado_filter = ''

    if competicion_id == 'todas' and fase_id == 'todas' or competicion_id == None and fase_id == None:
        encuentros = encuentro.objects.filter(estado_jugado=estado_filter)
        encuentrosParaFiltro = encuentro.objects.all()
    elif competicion_id != 'todas' and fase_id == 'todas':
        encuentros = encuentro.objects.filter(estado_jugado=estado_filter, competicion_id=competicion_id)
        encuentrosParaFiltro = encuentro.objects.filter(competicion_id=competicion_id)

    elif competicion_id == 'todas' and fase_id != 'todas':
        encuentros = encuentro.objects.filter(estado_jugado=estado_filter, fase_id=fase_id)
        encuentrosParaFiltro = encuentro.objects.all()
        if fase_id == '1' and grupo_id != 'todas':
            encuentros = encuentros.filter(grupo_id=grupo_id)
    else:
        encuentros = encuentro.objects.filter(estado_jugado=estado_filter, competicion_id=competicion_id, fase_id=fase_id)
        encuentrosParaFiltro = encuentro.objects.filter(competicion_id=competicion_id)
       
        if fase_id == '1' and grupo_id != 'todas':
            encuentros = encuentros.filter(grupo_id=grupo_id)

    fases = fase.objects.filter(fase_id__in=encuentrosParaFiltro.values('fase_id')).distinct()
    grupos = grupo.objects.filter(grupo_id__in=encuentrosParaFiltro.values('grupo_id')).distinct().order_by('grupo_id')
    print(fase_id)
    print(competicion_id)
    print(grupos)
    print(encuentros.values('grupo'))

    # Obtén las opciones para los combobox de filtro
    competiciones = competicion.objects.all()
    
    return render(
        request,
        'listarEncuentros.html',
        {
            'encuentros': encuentros,
            'tipo': tipo,
            'fases':fases,
            'competiciones': competiciones,
            'competicion_id':competicion_id,
            'fase_id':fase_id,
            'grupos':grupos,
            'grupo_id':grupo_id,
        }
    )


def asignar(request, tipo, encuentro_id):
    if tipo == 'alineaciones':
        return render(request, 'asignarAlineaciones.html', {'encuentro_id': encuentro_id})
    elif tipo == 'terna_arbitral':
        return render(request, 'asignar_terna_arbitral.html', {'encuentro_id': encuentro_id})
    elif tipo == 'eventos':
        return render(request, 'asignarEventos.html', {'encuentro_id': encuentro_id})
    elif tipo == 'estadisticas':
        return render(request, 'asignarEstadisticas.html', {'encuentro_id': encuentro_id})
    else:
# Manejo de error o redirección predeterminada
        return render(request, 'asignarAlineaciones.html', {'encuentro_id': encuentro_id})



def asignarAlineacion(request, encuentro_id):
    encuentro_obj = encuentro.objects.get(encuentro_id=encuentro_id)
    equipoLocal = equipo.objects.get(nombre=encuentro_obj.equipo_local)
    equipoVisita = equipo.objects.get(nombre=encuentro_obj.equipo_visita)
    contratoLocal = contrato.objects.filter(
        nuevo_club=equipoLocal.equipo_id).exclude(persona__tipo_persona_id=2)
    contratoVisita = contrato.objects.filter(
        nuevo_club=equipoVisita.equipo_id).exclude(persona__tipo_persona_id=2)
    # Verificar si ya hay alineaciones registradas para este encuentro
    alineaciones_local = alineacion.objects.filter(
        descripcion_encuentro_id__encuentro=encuentro_obj, descripcion_encuentro_id__equipo=equipoLocal, estado=True)
    alineaciones_visita = alineacion.objects.filter(
        descripcion_encuentro_id__encuentro=encuentro_obj, descripcion_encuentro_id__equipo=equipoVisita,estado=True)
    # Obtener los IDs de los jugadores en la alineación para este encuentro específico
    jugadores_en_alineacion_local = set(
        alineaciones_local.values_list('contrato_id__persona_id', flat=True))
    jugadores_en_alineacion_visita = set(
        alineaciones_visita.values_list('contrato_id__persona_id', flat=True))
    
    capitan_actual_local = None  # Inicializa la variable antes del bucle
    capitan_actual_visita = None  # Inicializa la variable antes del bucle
    alineacion_capitan_local = alineacion.objects.filter(
        descripcion_encuentro_id__encuentro=encuentro_obj,
        descripcion_encuentro_id__equipo=equipoLocal,
        capitan=True,
        estado=True
    ).first()

    if alineacion_capitan_local:
        capitan_actual_local = alineacion_capitan_local.contrato_id.persona_id

    alineacion_capitan_visita = alineacion.objects.filter(
        descripcion_encuentro_id__encuentro=encuentro_obj,
        descripcion_encuentro_id__equipo=equipoVisita,
        capitan=True,
        estado=True
    ).first()

    if alineacion_capitan_visita:
        capitan_actual_visita = alineacion_capitan_visita.contrato_id.persona_id

            
    # Obtener formación actual de cada equipo
    formacion_local_actual = alineaciones_local.first(
    ).formacion if alineaciones_local.exists() else '4-3-3'
    formacion_visita_actual = alineaciones_visita.first(
    ).formacion if alineaciones_visita.exists() else '4-3-3'

    if request.method == 'POST':

        jugadoresLocales=  request.POST.getlist('jugadoresLocales[]', [])
        jugadoresVisitas=  request.POST.getlist('jugadoresVisitas[]', [])
        jugadores_local_sel = request.POST.getlist('jugadores_local[]', [])
        jugadores_visita_sel = request.POST.getlist('jugadores_visita[]', [])
        formacion_local = request.POST.get('formacion_local', '4-3-3')
        formacion_visita = request.POST.get('formacion_visita', '4-3-3')

        capitan_local = request.POST.get('capitan_local', None)
        capitan_visita = request.POST.get('capitan_visita', None)
        # Validate that both teams have exactly 11 players
        if len(jugadores_local_sel) != 11 or len(jugadores_visita_sel) != 11:
            messages.success(
                request, 'Debe seleccionar exactamente 11 jugadores por equipo.')
            return redirect(f"/appPartido/asignar/alineaciones/{encuentro_id}/")

        # Obtener descripciones de encuentro local y visita
        descripcion_encuentro_local = descripcion_encuentro.objects.filter(
            equipo=equipoLocal, encuentro=encuentro_obj).first()
        descripcion_encuentro_visita = descripcion_encuentro.objects.filter(
            equipo=equipoVisita, encuentro=encuentro_obj).first()
        # Guardar jugadores del equipo local
        alineacion.objects.filter(descripcion_encuentro_id__encuentro=encuentro_obj).delete()
    
        for jugador_id_local in jugadoresLocales[:40]:
            if jugador_id_local:
                contrato_local = contrato.objects.filter(
                    persona_id=jugador_id_local).first()
                posicionLocal = posicion_jugador.objects.get(
                    posicion_jugador_id=contrato_local.posicion_jugador.posicion_jugador_id)
                for i in jugadores_local_sel[:11]:
                    estadoJugadorLocal = (jugador_id_local == i)
                    if estadoJugadorLocal == False:
                        estadoJugadorLocal = False
                    else:
                        break
                # Verifica si este jugador es el capitán
                capitanL = (jugador_id_local == capitan_local)
                alineacion_local = alineacion(
                    descripcion_encuentro_id=descripcion_encuentro_local,
                    contrato_id=contrato_local,
                    dorsal=contrato_local.dorsal,
                    posicion_jugador_id=posicionLocal,
                    capitan=capitanL,  # Usa el valor booleano aquí
                    estado=estadoJugadorLocal,
                    formacion=formacion_local
                )
                alineacion_local.save()
       
        # Guardar jugadores del equipo visitante
        for jugador_id_visita in jugadoresVisitas[:40]:
                if jugador_id_visita:
                    contrato_visita = contrato.objects.filter(
                        persona_id=jugador_id_visita).first()
                    posicionVisita = posicion_jugador.objects.get(
                        posicion_jugador_id=contrato_visita.posicion_jugador.posicion_jugador_id)
                    for i in jugadores_visita_sel[:11]:
                        estadoJugadorVisita = (jugador_id_visita == i)
                        if estadoJugadorVisita == False:
                            estadoJugadorVisita = False
                        else:
                            break    
                        # Verifica si este jugador es el capitán
                    capitanV = (jugador_id_visita == capitan_visita)
                    alineacion_visita = alineacion(
                        descripcion_encuentro_id=descripcion_encuentro_visita,
                        contrato_id=contrato_visita,
                        dorsal=contrato_visita.dorsal,
                        posicion_jugador_id=posicionVisita,
                        capitan=capitanV, 
                        estado=estadoJugadorVisita,
                        formacion=formacion_visita
                    )
                    alineacion_visita.save()

        messages.success(request, 'Alineaciones guardadas correctamente.')
        return redirect("/appPartido/lista_encuentros/?tipo=alineaciones")

    return render(request, 'asignarAlineaciones.html', {
        'encuentro': encuentro_obj,
        'equipoLocal': contratoLocal,
        'equipoVisita': contratoVisita,
        'jugadores_en_alineacion_local': jugadores_en_alineacion_local,
        'jugadores_en_alineacion_visita': jugadores_en_alineacion_visita,
        'formacion_local_actual': formacion_local_actual,
        'formacion_visita_actual': formacion_visita_actual,
        'capitan_actual_local': capitan_actual_local,  
        'capitan_actual_visita': capitan_actual_visita, 
    })

def asignarEventos(request, encuentro_id):
    tipos_evento_relacionados = tipo_evento.objects.all()
    encuentro_obj = encuentro.objects.get(encuentro_id=encuentro_id)
    equipoLocal = equipo.objects.get(nombre=encuentro_obj.equipo_local)
    equipoVisita = equipo.objects.get(nombre=encuentro_obj.equipo_visita)

    descripcionEncuentroLocal_objs = descripcion_encuentro.objects.filter(
        equipo=encuentro_obj.equipo_local, encuentro=encuentro_obj)
    descripcionEncuentroVisita_objs = descripcion_encuentro.objects.filter(
        equipo=encuentro_obj.equipo_visita, encuentro=encuentro_obj)
    alineacion01 = alineacion.objects.filter(
        descripcion_encuentro_id__in=descripcionEncuentroLocal_objs)
    alineacion02 = alineacion.objects.filter(
        descripcion_encuentro_id__in=descripcionEncuentroVisita_objs)
    eventos = evento.objects.filter(encuentro_id=encuentro_id)

    tipo_evento_id = None  # Inicializar la variable fuera del bloque condicional
   
        
    if request.method == 'POST':
        tipo_evento_id = request.POST.get('tipos_evento_relacionados')
        evento_equipo = request.POST.get('equipo')
        print('tipo',tipo_evento_id)
        print('equipo',evento_equipo)
        if tipo_evento_id == '3':
            if evento_equipo == 'Local':
                alineacion01 = alineacion.objects.filter(descripcion_encuentro_id__in=descripcionEncuentroLocal_objs, estado=True)
                alineacion02 = alineacion.objects.filter(descripcion_encuentro_id__in=descripcionEncuentroLocal_objs, estado=False)
            elif evento_equipo == 'Visita':
                alineacion01 = alineacion.objects.filter(descripcion_encuentro_id__in=descripcionEncuentroVisita_objs, estado=True)
                alineacion02 = alineacion.objects.filter(descripcion_encuentro_id__in=descripcionEncuentroVisita_objs, estado=False)
        else:
            if evento_equipo == 'Local':
                alineacion01 = alineacion.objects.filter(descripcion_encuentro_id__in=descripcionEncuentroLocal_objs)
                alineacion02 = alineacion.objects.filter( descripcion_encuentro_id__in=descripcionEncuentroVisita_objs)
            elif evento_equipo == 'Visita':
                alineacion01 = alineacion.objects.filter( descripcion_encuentro_id__in=descripcionEncuentroVisita_objs)
                alineacion02 = alineacion.objects.filter(descripcion_encuentro_id__in=descripcionEncuentroLocal_objs)

        if 'guardar_evento' in request.POST:
            # tipo_evento_id = request.POST.get('tipo_evento_seleccionado', None)

            alineacion011 = request.POST.get('alineacion01', None)
            alineacion021 = request.POST.get('alineacion02', None)
            tiempo = request.POST.get('tiempo', 0)
            tiempo = int(tiempo) if tiempo else 0
            tiempo_extra = request.POST.get('tiempo_extra', 0)
            tiempo_extra = int(tiempo_extra) if tiempo_extra else 0
            motivo = request.POST.get('motivo', '')
            encuentro_id = int(encuentro_id) if encuentro_id else 0
            evento_equipo=request.POST.get('equipo')
            equipoSe = (evento_equipo=='Local')

            alineacion_id1 = alineacion.objects.get(alineacion_id=alineacion011) if alineacion011 else None
            alineacion_id2 = alineacion.objects.get(alineacion_id=alineacion021) if alineacion021 else None
            

                    
            evento_obj = evento(
                tipo_evento_id=tipo_evento.objects.get(tipo_evento_id=tipo_evento_id),
                alineacion_id1=alineacion_id1,
                alineacion_id2=alineacion_id2,
                encuentro_id=encuentro_obj,
                evento_equipo=equipoSe,
                motivo=motivo,
                tiempo=tiempo,
                tiempo_extra=tiempo_extra,
            )
            evento_obj.save()

            messages.success(request, 'Eventos guardados correctamente.')
        elif 'eliminar_evento' in request.POST:
                # Lógica para eliminar un detalle de la terna arbitral
                evento_id = int(request.POST.get('eliminar_evento'))
                evento_obj = get_object_or_404(evento, pk=evento_id)
                print(f"Eliminando evento con ID {evento_id}")

                evento_obj.delete()
                print(f"Evento eliminado correctamente")
            # return redirect(f'/appPartido/asignar/eventos/{evento_id}/')
            

    return render(request, 'asignarEventos.html', {
        'fecha_encuentro': encuentro_obj.fecha,
        'encuentro_id': encuentro_id,
        'equipoLocal': equipoLocal,
        'equipoVisita': equipoVisita,
        'eventos': eventos,
        'tipos_evento_relacionados': tipos_evento_relacionados,
        'alineacion01': alineacion01,
        'alineacion02': alineacion02,
    })
    
    
def asignarEstadisticas(request, encuentro_id):
    encuentro_obj = encuentro.objects.get(encuentro_id=encuentro_id)
    equipoLocal = equipo.objects.get(nombre=encuentro_obj.equipo_local)
    equipoVisita = equipo.objects.get(nombre=encuentro_obj.equipo_visita)
    descripcion_encuentro_local = descripcion_encuentro.objects.filter(equipo=equipoLocal).first()
    descripcion_encuentro_visita = descripcion_encuentro.objects.filter(equipo=equipoVisita).first()

    estadistica_local, created_local = estadisticas.objects.get_or_create(
        descripcion_encuentro_id=descripcion_encuentro_local,
        defaults={
            'posesion_balon': 0,
            'pases_acertados': 0,
            'tiros_desviados': 0,
            'efectividad_pases': 0,
            'tiros_indirectos_arco': 0,
            'tiros_directos_arco': 0,
        }
    )
    estadistica_visitante, created_visitante = estadisticas.objects.get_or_create(
        descripcion_encuentro_id=descripcion_encuentro_visita,
        defaults={
            'posesion_balon': 0,
            'pases_acertados': 0,
            'tiros_desviados': 0,
            'efectividad_pases': 0,
            'tiros_indirectos_arco': 0,
            'tiros_directos_arco': 0,
        }
    )

    if request.method == 'POST':
        # Actualiza los valores de las estadísticas locales
        estadistica_local.posesion_balon = request.POST.get('posesion_balon_equipo1', 0)
        estadistica_local.pases_acertados = request.POST.get('pases_acertados_equipo1', 0)
        estadistica_local.tiros_desviados = request.POST.get('tiros_desviados_equipo1', 0)
        estadistica_local.efectividad_pases = request.POST.get('efectividad_pases_equipo1', 0)
        estadistica_local.tiros_indirectos_arco = request.POST.get('tiros_indirectos_arco_equipo1', 0)
        estadistica_local.tiros_directos_arco = request.POST.get('tiros_directos_arco_equipo1', 0)

        # Actualiza los valores de las estadísticas visitantes
        estadistica_visitante.posesion_balon = request.POST.get('posesion_balon_equipo2', 0)
        estadistica_visitante.pases_acertados = request.POST.get('pases_acertados_equipo2', 0)
        estadistica_visitante.tiros_desviados = request.POST.get('tiros_desviados_equipo2', 0)
        estadistica_visitante.efectividad_pases = request.POST.get('efectividad_pases_equipo2', 0)
        estadistica_visitante.tiros_indirectos_arco = request.POST.get('tiros_indirectos_arco_equipo2', 0)
        estadistica_visitante.tiros_directos_arco = request.POST.get('tiros_directos_arco_equipo2', 0)

        estadistica_local.save()
        estadistica_visitante.save()

        messages.success(request, 'Estadísticas guardadas exitosamente')

    return render(request, 'asignarEstadisticas.html', {
        'encuentro': encuentro_obj,
        'equipoLocal': equipoLocal,
        'equipoVisita': equipoVisita,
        'estadistica_local': estadistica_local,
        'estadistica_visitante': estadistica_visitante,
    })


def asignar_terna_arbitral(request, encuentro_id):
    encuentro_obj = encuentro.objects.get(encuentro_id=encuentro_id)
    arbitros = persona.objects.filter(tipo_persona_id__descripcion='ARBITRO') 
    tipos_arbitro = tipo_arbitro.objects.all()
    detalles_terna = detalle_terna.objects.filter(encuentro_id=encuentro_id)


    
    if request.method == 'POST':
        if 'añadir_detalle' in request.POST:
            # Lógica para guardar los detalles de la terna arbitral
            arbitro_id = int(request.POST.get('arbitro'))
            arbitro = persona.objects.get(persona_id=arbitro_id)
            tipo_arbitro_id = int(request.POST.get('tipo_arbitro'))
            tipo_arbitro_obj = tipo_arbitro.objects.get(tipo_arbitro_id=tipo_arbitro_id)
            
            # Aquí deberías crear un objeto detalle_terna y guardarlo en la base de datos
            detalle = detalle_terna(persona_id=arbitro, tipo_arbitro_id=tipo_arbitro_obj, encuentro_id=encuentro_obj)
            detalle.save()
            messages.success(request, 'Detalle añadido correctamente.')

        elif 'eliminar_detalle' in request.POST:
            # Lógica para eliminar un detalle de la terna arbitral
            detalle_id = int(request.POST.get('eliminar_detalle'))
            detalle = get_object_or_404(detalle_terna, pk=detalle_id)
            detalle.delete()


        return redirect(f"/appPartido/asignar/terna_arbitral/{encuentro_id}/")

    return render(request, 'asignar_terna_arbitral.html', {'encuentro': encuentro_obj, 'arbitros': arbitros, 'tipos_arbitro': tipos_arbitro,'detalles_terna': detalles_terna})
