from email.policy import default
from random import choices
from django.db import models
from django import forms
from appEquipo.models import alineacion

# Create your models here.


class ciudad(models.Model):
    ciudad_id=models.BigAutoField(primary_key=True)
    nombre=models.CharField(max_length=30)
    norma=models.CharField(max_length=5)
    pais_id=models.ForeignKey('appCompeticion.pais',on_delete=models.CASCADE,db_column='pais_id')

    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        self.norma = self.norma.upper()
        super(ciudad, self).save(force_insert, force_update)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural='ciudad'

class sede(models.Model):
    CHOICE_ESTADO_SEDE=[
        ('SD','SUSPENDIDO DEFINITIVAMENTE'),
        ('DI','DISPONIBLE'),
        ('EM','EN MANTENIMIENTO'),
        ('ND','NO DISPONIBLE'),
        ('ST','SUSPENDIDO TEMPORALMENTE')
    ]
    sede_id=models.BigAutoField(primary_key=True)
    nombre=models.CharField(max_length=255)
    alias=models.CharField(max_length=100)
    capacidad=models.IntegerField()
    fecha_inauguracion=models.DateField()
    ciudad_id=models.ForeignKey(ciudad, on_delete=models.CASCADE,db_column='ciudad_id')
    imagen = models.ImageField(null=True, blank=True, upload_to='sede/', default = 'sede/imagen_default.png')
    # CHOICE_ESTADO_SEDE| SD= SUSPENDIDO TEMPORALMENTE, DI= DISPONIBLE , EM = EN MANTENIMIENTO, ND = NO DISPONIBLE, ST = SUSPENDIDO TEMPORALMENTE
    estado=models.CharField(max_length=2,default='DI',choices=CHOICE_ESTADO_SEDE)

    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        self.alias = self.alias.upper()
        super(sede, self).save(force_insert, force_update)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural='sede'

##NUEVO
class descripcion_encuentro(models.Model):
    CHOICE_EQUIPO = [
        ('L', 'LOCAL'),
        ('V', 'VISITA')
    ]

    descripcion_encuentro_id = models.BigAutoField(primary_key=True)
    tipo_equipo = models.CharField(max_length=10, choices=CHOICE_EQUIPO,  blank=True, null=True)
    goles = models.CharField(max_length=4, blank=True, null=True)
    goles_ronda_penales = models.CharField(max_length=4 , blank=True, null=True)
    equipo = models.ForeignKey('appEquipo.equipo', on_delete=models.CASCADE, db_column='equipo_id', related_name='descripcion_encuentros', blank=True, null=True)
    encuentro = models.ForeignKey('encuentro', on_delete=models.CASCADE, db_column='encuentro_id', related_name='descripcion_encuentros', blank=True, null=True)

    def save(self, force_insert=False, force_update=False):
        super(descripcion_encuentro, self).save(force_insert, force_update)

    def __str__(self):
        return str(self.equipo)
    class Meta:
        verbose_name_plural = 'descripcion_encuentro'


class encuentro(models.Model):
    CHOICE_ESTADO = [
         ('J', 'JUGADO'),
         ('N', 'NO JUGADO'),
         ('E', 'EN JUEGO'),
         ('S', 'SUSPENDIDO'),
     ]
    CHOICE_RESULTADO = [
         ('L', 'LOCAL'),
         ('E', 'EMPATE'),
         ('V', 'VISITA'),
     ]

    encuentro_id=models.BigAutoField(primary_key=True)
    competicion_id=models.ForeignKey("appCompeticion.competicion", on_delete=models.CASCADE,db_column='competicion_id')
    sede_id=models.ForeignKey(sede,on_delete=models.CASCADE,db_column='sede_id',blank=True,null=True)
    fase=models.ForeignKey("appCompeticion.fase", on_delete=models.CASCADE,db_column='fase',related_name='fase')
    grupo=models.ForeignKey("appCompeticion.grupo", on_delete=models.CASCADE,db_column='grupo',related_name='grupo',blank=True,null=True)
    jornada=models.ForeignKey("appCompeticion.jornada", on_delete=models.CASCADE,db_column='jornada',related_name='jornada',blank=True,null=True)
    resultado=models.CharField(max_length=1,null=True,blank=True,choices=CHOICE_RESULTADO)
    equipo_local=models.ForeignKey('appEquipo.equipo', on_delete=models.CASCADE,db_column='equipo_local',related_name='equipo_local')
    equipo_visita=models.ForeignKey('appEquipo.equipo', on_delete=models.CASCADE,db_column='equipo_visita',related_name='equipo_visita')
    fecha=models.DateTimeField(blank=True,null=True)
    clima=models.CharField(max_length=4)
    estado_jugado=models.CharField(max_length=10,default='N',choices=CHOICE_ESTADO, null=True)

    def save(self, force_insert=False, force_update=False):
        
        self.clima = self.clima.upper()
        super(encuentro, self).save(force_insert, force_update)
        
    def __str__(self):
        
        return str(self.equipo_local) + " vs " + str(self.equipo_visita)

    class Meta:
        verbose_name_plural = 'encuentro'

## FIN

# class detalle_encuentro(models.Model):
#     CHOICE_TIPO_EQUIPO= [
#         ('L','LOCAL'),
#         ('V','VISITA'),
#     ]

#     detalle_encuentro_id=models.BigAutoField(primary_key=True)
#     encuentro_id=models.ForeignKey('encuentro',on_delete=models.CASCADE,db_column='encuentro_id')
#     equipo_id=models.ForeignKey('appEquipo.equipo', on_delete=models.CASCADE,db_column='equipo_id')
#     formacion_id=models.ForeignKey('formacion',on_delete=models.CASCADE,db_column='formacion_id')
#     # CHOICE_TIPO_EQUIPO | L = LOCAL | V = VISITA
#     tipo_equipo=models.CharField(max_length=1,choices=CHOICE_TIPO_EQUIPO)
#     resultado=models.CharField(max_length=3)

#     def __str__(self):
#         return str(self.detalle_encuentro_id)

#     class Meta:
#         verbose_name_plural='detalle_encuentro'
    
class tipo_evento(models.Model):
    tipo_evento_id=models.BigAutoField(primary_key=True)
    nombre=models.CharField(max_length=30)
    descripcion=models.CharField(max_length=300)
    estado=models.BooleanField()
    logo_tipo_evento=models.ImageField(blank=True,null=True,upload_to='jugador/',default='jugador/logo_default.png')
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        self.descripcion = self.descripcion.upper()
        super(tipo_evento, self).save(force_insert, force_update)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural='tipo_evento'

class evento(models.Model):
    evento_id = models.BigAutoField(primary_key=True)
    tipo_evento_id = models.ForeignKey(tipo_evento, on_delete=models.CASCADE, db_column='tipo_evento_id', null=True)
    encuentro_id = models.ForeignKey(encuentro, on_delete=models.CASCADE, db_column='encuentro_id', null=True)
    alineacion_id1 = models.ForeignKey("appEquipo.alineacion", on_delete=models.CASCADE, db_column='alineacion_id1', null=True, related_name='eventos_alineacion1', blank=True)
    alineacion_id2 = models.ForeignKey("appEquipo.alineacion", on_delete=models.CASCADE, db_column='alineacion_id2', null=True, related_name='eventos_alineacion2', blank=True)
    tiempo = models.IntegerField(null=True, blank=True)
    tiempo_extra = models.IntegerField(null=True, blank=True)
    motivo=models.CharField(max_length=255, null=True, blank=True)
    evento_equipo = models.BooleanField()

    def save(self, force_insert=False, force_update=False):
        super(evento, self).save(force_insert, force_update)

    def __str__(self):
        return str(self.evento_id)

    class Meta:
        verbose_name_plural = 'evento'

class estadisticas(models.Model):
       
    estadisticas_id=models.BigAutoField(primary_key=True)
    posesion_balon=models.IntegerField()
    pases_acertados=models.IntegerField()
    tiros_desviados=models.IntegerField()
    efectividad_pases=models.IntegerField()
    tiros_indirectos_arco=models.IntegerField()
    tiros_directos_arco=models.IntegerField()
    descripcion_encuentro_id = models.ForeignKey(descripcion_encuentro, on_delete=models.CASCADE, db_column='descripcion_encuentro_id', null=True)

    def _str_(self):
        return str(self.estadisticas_id)

    class Meta:
        verbose_name_plural='estadisticas'
