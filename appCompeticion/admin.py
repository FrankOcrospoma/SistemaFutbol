from django.contrib import admin
from appCompeticion.models import *

# Register your models here.

class competicionAdmin(admin.ModelAdmin):
    list_display=['nombre','organizacion_id','logo_competicion','pais_id']
    ordering=['nombre']
    search_fields = ['nombre']
    list_filter=['nombre']
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)   
class paisAdmin(admin.ModelAdmin):
    list_display = ['nombre','sigla','logo_bandera']
    ordering = ['nombre']
    search_fields = ['nombre','sigla']
    list_per_page=6
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)   
class deporteAdmin(admin.ModelAdmin):
    list_display=['nombre','estado']
    ordering=['deporte_id']
    search_fields = ['nombre']
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)   
class grupoAdmin(admin.ModelAdmin):
    list_display=['nombre']
    ordering=['nombre']
    search_fields = ['nombre']
    list_per_page =4
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)   
class jornadaAdmin(admin.ModelAdmin):
    list_display=['nombre']
    ordering=['nombre']
    search_fields = ['nombre']
    list_per_page =4
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)   

class faseAdmin(admin.ModelAdmin):
    list_display=['nombre']
    ordering=['nombre']
    search_fields=['nombre']
    list_per_page =4
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)    

class detalle_grupoAdmin(admin.ModelAdmin):
    list_display=['competicion_id','fase_id','grupo_id','equipo_id']
    search_fields = ['equipo_id__nombre','grupo_id__nombre','competicion_id__nombre']
    ordering =['competicion_id']
    list_per_page =4
    list_filter=['competicion_id','fase_id','grupo_id']
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)

class tablaAdmin(admin.ModelAdmin):
    list_display=['competicion_id','equipo_id','ganado','perdido','empatado','goles_favor','goles_contra','tarjetas_amarillas','tarjetas_rojas','puntos']
    ordering=['-puntos']
    search_fields = ['equipo_id__nombre']
    list_filter=['competicion_id']
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)
class organizacionAdmin(admin.ModelAdmin):
    list_display=['nombre_oficial','siglas','descripcion','tipo','estado','logo']
    ordering=['nombre_oficial']
    search_fields = ['nombre_oficial']
    list_per_page=4
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)
class patrocinadorAdmin(admin.ModelAdmin):
    list_display=['nombre_patrocinador','nombre_abreviado','descripcion','estado','logo_1','logo_2']
    ordering=['nombre_patrocinador']
    search_fields=['nombre_patrocinador','nombre_abreviado']
    list_per_page=5
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)
class detalle_patrocinadorAdmin(admin.ModelAdmin):
    list_display=['competicion_id']
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)
admin.site.register(competicion,competicionAdmin)
admin.site.register(pais,paisAdmin)
admin.site.register(deporte,deporteAdmin)
admin.site.register(grupo,grupoAdmin)
admin.site.register(jornada,jornadaAdmin)

admin.site.register(fase,faseAdmin)
admin.site.register(detalle_grupo,detalle_grupoAdmin)
admin.site.register(tabla_posicion,tablaAdmin)
admin.site.register(organizacion,organizacionAdmin)
admin.site.register(patrocinador,patrocinadorAdmin)
admin.site.register(detalle_patrocinador,detalle_patrocinadorAdmin)