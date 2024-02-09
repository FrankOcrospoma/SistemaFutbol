from django.contrib import admin
from django.db import models
from django.forms import TextInput, ModelForm
from django.utils.html import format_html
from appEquipo.models import *

# Register your models here.

class categoriaEquipo(admin.ModelAdmin):
    list_display=['nombre']
    ordering=['nombre']
    search_fields=['nombre']
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)
class equipoForm(ModelForm):
    class Meta:
        model = equipo
        exclude = ('deporte_id',)
        widgets = {
            'vestimenta_principal_color_principal': TextInput(attrs={'type': 'color'}),
            'vestimenta_principal_color_secundario': TextInput(attrs={'type': 'color'}),
            'vestimenta_alterna_color_principal': TextInput(attrs={'type': 'color'}),
            'vestimenta_alterna_color_secundario': TextInput(attrs={'type': 'color'}),
        }

class equipoAdmin(admin.ModelAdmin):
    form = equipoForm
    def color_vestimenta_principal_principal(self, obj):
        return format_html(
            '<div style="width: 30px; height: 20px; background-color: {}"></div>',
            obj.vestimenta_principal_color_principal
        )

    def color_vestimenta_principal_secundario(self, obj):
        return format_html(
            '<div style="width: 30px; height: 20px; background-color: {}"></div>',
            obj.vestimenta_principal_color_secundario
        )

    def color_vestimenta_alterna_principal(self, obj):
        return format_html(
            '<div style="width: 30px; height: 20px; background-color: {}"></div>',
            obj.vestimenta_alterna_color_principal
        )

    def color_vestimenta_alterna_secundario(self, obj):
        return format_html(
            '<div style="width: 30px; height: 20px; background-color: {}"></div>',
            obj.vestimenta_alterna_color_secundario
        )
    list_display = ['nombre', 'presidente', 'logo', 'color_vestimenta_principal_principal','color_vestimenta_principal_secundario',
                    'color_vestimenta_alterna_principal','color_vestimenta_alterna_secundario', 'portada', 'siglas',
                    'categoria_equipo', 'tipo_equipo_id', 'sede_id','entrenador_id']
    ordering = ['nombre']
    search_fields = ['nombre']
    list_per_page=5
    list_filter=['categoria_equipo','tipo_equipo_id','entrenador_id']
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)
class tipoEquipoAdmin(admin.ModelAdmin):
    list_display=['descripcion','estado']
    ordering=['tipo_equipo_id']
    search_fields = ['descripcion']
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)
class posicionJugadorAdmin(admin.ModelAdmin):
    list_display=['descripcion']
    ordering=['descripcion']
    search_fields = ['descripcion']
    list_per_page=5
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js','assets/js/control_botones.js','assets/js/editar_botones.js',)
class alineacionAdmin(admin.ModelAdmin):
    list_display=['alineacion_id','fecha_juego','descripcion','estado']
    ordering=['alineacion_id']
    search_fields=['descripcion']

class AlineacionEquipoAdmin(admin.ModelAdmin):
    list_display=['posicion_jugador_id','dorsal','contrato_id','capitan','estado']
    ordering=['posicion_jugador_id']
    search_fields = ['posicion_jugador_id__descripcion','dorsal']
    list_filter = ['descripcion_encuentro_id__encuentro','descripcion_encuentro_id__equipo','capitan']


    class Media:
        js = ('https://code.jquery.com/jquery-3.6.4.min.js', 'assets/js/alineacion_admin.js','assets/js/control_botones.js','assets/js/editar_botones.js',)


admin.site.register(categoria_equipo,categoriaEquipo)
admin.site.register(tipo_equipo,tipoEquipoAdmin)
admin.site.register(equipo,equipoAdmin)
admin.site.register(posicion_jugador,posicionJugadorAdmin)
admin.site.register(alineacion,AlineacionEquipoAdmin)

