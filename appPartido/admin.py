from django.contrib import admin
from appPartido.models import *



class sedeAdmin(admin.ModelAdmin):
    list_display=['nombre','alias','capacidad','fecha_inauguracion','ciudad_id', 'imagen','estado']
    ordering=['nombre']
    search_fields = ['nombre']
    list_per_page=5
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)
##
class descripcionEncuentroAdmin(admin.ModelAdmin):
    list_display=['encuentro','equipo','goles','goles_ronda_penales']
    ordering=['encuentro']
    search_fields = ['equipo_id__nombre']
    list_per_page=5
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)

class encuentroAdmin(admin.ModelAdmin):
    list_display = ['competicion_id', 'equipo_local', 'equipo_visita', 'sede_id', 'fase', 'fecha', 'clima', 'estado_jugado', 'resultado']
    ordering = ['competicion_id']
    search_fields = ['sede_id__nombre', 'competicion_id__nombre', 'equipo_local__nombre', 'equipo_visita__nombre', 'encuentro_id']
    list_per_page = 6
    list_filter = ['competicion_id', 'grupo', 'fase', 'estado_jugado']


    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js', 'assets/js/control_botones.js', 'assets/js/editar_botones.js',)

# class detalleEncuentroAdmin(admin.ModelAdmin):
#     list_display=['detalle_encuentro_id','encuentro_id','equipo_id','formacion_id','tipo_equipo','resultado']
#     ordering=['detalle_encuentro_id']
#     search_fields=['equipo_id','encuentro_id']

class tipo_eventoAdmin(admin.ModelAdmin):
    list_display=['nombre','descripcion','estado','logo_tipo_evento']
    ordering=['nombre']
    search_fields = ['nombre','tipo_evento_id']
    list_per_page=5
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)



class eventoAdmin(admin.ModelAdmin):
    list_display = [ 'tipo_evento_id', 'encuentro_id', 'tiempo','alineacion_id1','alineacion_id2']
    ordering = ['tipo_evento_id']
    search_fields = ['encuentro_id__equipo_local__nombre', 'encuentro_id__equipo_visita__nombre']
    list_filter = ['encuentro_id__competicion_id']
  
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js', 'assets/js/evento_admin.js','assets/js/control_botones.js','assets/js/editar_botones.js',)


admin.site.register(sede,sedeAdmin)
admin.site.register(descripcion_encuentro,descripcionEncuentroAdmin)
admin.site.register(encuentro,encuentroAdmin)
# admin.site.register(detalle_encuentro,detalleEncuentroAdmin)
admin.site.register(tipo_evento,tipo_eventoAdmin)
# admin.site.register(evento,eventoAdmin)