from django.contrib import admin
from appContrato.models import *

# Register your models here.
class tipo_personaAdmin(admin.ModelAdmin):
    list_display = ['descripcion']
    ordering = ['descripcion']
    search_fields = ['descripcion']
    
    class Media:
        js = (
            'https://code.jquery.com/jquery-3.6.4.min.js',
            'assets/js/control_botones.js',
            'assets/js/editar_botones.js',  # Agrega el nuevo script aquí
        )

class personaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'alias', 'sexo', 'fecha_nacimiento', 'ciudad_id', 'estatura', 'peso', 'tipo_persona_id', 'estado', 'foto','organizacion_id']
    ordering = ['nombre']
    search_fields = ['nombre', 'apellido', 'alias']
    list_per_page = 11
    list_filter = ['tipo_persona_id', 'contratos_persona__nuevo_club']  
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)

class contratoAdmin(admin.ModelAdmin):
    list_display=['tipo_contrato','persona','fecha_inicio', 'fecha_fin', 'valor','nuevo_club','posicion_jugador','dorsal','estado']
    ordering = ['persona']
    search_fields = ['persona_id__nombre']
    list_filter=['tipo_contrato', 'nuevo_club','estado']
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)   

class tipoArbitroAdmin(admin.ModelAdmin):
    list_display=['nombre','estado']
    ordering=['nombre']
    search_fields = ['nombre']
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)
class detalleTernaArbitralAdmin(admin.ModelAdmin):
    list_display=['tipo_arbitro_id', 'persona_id','encuentro_id']
    ordering=['encuentro_id']
    search_fields = ['tipo_arbitro_id__nombre']
    list_per_page=5
    list_filter=['tipo_arbitro_id','encuentro_id']
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)   

admin.site.register(tipo_persona,tipo_personaAdmin)
admin.site.register(persona,personaAdmin)
admin.site.register(contrato,contratoAdmin)
admin.site.register(tipo_arbitro,tipoArbitroAdmin)
# admin.site.register(detalle_terna,detalleTernaArbitralAdmin)