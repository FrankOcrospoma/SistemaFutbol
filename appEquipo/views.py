from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .models import *
from .admin import *
from appPartido.models import *
from appContrato.models import *

class ObteneraJugadoresView(View):
    def get(self, request, *args, **kwargs):
        de_id = request.GET.get('descripcion_encuentro_id')

        try:
            descripcion_encuentro_obj = descripcion_encuentro.objects.get(descripcion_encuentro_id=de_id)
            equipos = equipo.objects.get(nombre=descripcion_encuentro_obj.equipo)

            contratos = contrato.objects.filter(nuevo_club=equipos.equipo_id)
        
            data = {contrato.contrato_id: str(contrato) for contrato in contratos}
            return JsonResponse(data)
        
        except Exception as e:
            print(f"Excepción no manejada: {str(e)}")
            return JsonResponse({"error": "Error interno del servidor."}, status=500)

