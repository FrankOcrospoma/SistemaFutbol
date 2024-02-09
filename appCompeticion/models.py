from email.policy import default
from django.db import models
from django import forms

# Create your models here.

PAIS_CHOICES = (
    ('SUSPENDIDO', 'Suspendido'),
    ('PROBACION', 'Probación'),
    ('NO_AFILIADO', 'No Afiliado'),
    ('SANCIONADO', 'Sancionado'),
    ('EN_INVESTIGACION', 'En Investigación'),
    ('MIEMBRO', 'Miembro'),
)

class pais(models.Model):
    pais_id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    sigla = models.CharField(max_length=3, default='')
    logo_bandera = models.ImageField(blank=True, null=True, upload_to='bandera/', default='bandera/bandera_default.png')

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.sigla = self.sigla.upper()
        super(pais, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = 'paises'



class deporte(models.Model):
    deporte_id=models.BigAutoField(primary_key=True)
    nombre=models.CharField(max_length=30)
    estado=models.BooleanField()

    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(deporte, self).save(force_insert, force_update)

    def __str__(self):
         return str(self.nombre)
        
    class Meta: 
        verbose_name_plural='deporte'

class patrocinador (models.Model):
    patrocinador_id=models.BigAutoField(primary_key=True)
    nombre_patrocinador=models.CharField(max_length=50)
    nombre_abreviado=models.CharField(max_length=10)
    descripcion=models.TextField()
    estado=models.BooleanField()
    logo_1=models.ImageField(blank=True,upload_to='patrocinador/logo_1/',default='patrocinador/logo_1/logo_default.png')
    logo_2=models.ImageField(blank=True,upload_to='patrocinador/logo_2/',default='patrocinador/logo_2/logo_default.png')

    def save(self, force_insert=False, force_update=False):
        self.nombre_patrocinador = self.nombre_patrocinador.upper()
        self.nombre_abreviado = self.nombre_abreviado.upper()
        super(patrocinador, self).save(force_insert, force_update)

    def __str__(self):
         return str(self.nombre_patrocinador)
        
    class Meta: 
        verbose_name_plural='patrocinador'

class organizacion(models.Model):
       
    CHOICE_TIPO = [
        ('F', 'FEDERACIÓN NACIONAL'),
        ('I', 'FEDERACIÓN INTERNACIONAL'),
        ('C', 'CONFEDERACIÓN'),
        ('L', 'LIGA'),
        ('A', 'ASOCIACIÓN'),
        
    ]
    organizacion_id=models.BigAutoField(primary_key=True)
    nombre_oficial=models.CharField(max_length=200)
    siglas=models.CharField(max_length=10,default='')
    descripcion=models.CharField(max_length=200)
    tipo=models.CharField(max_length=1,choices=CHOICE_TIPO, default='I')
    estado=models.BooleanField()
    logo=models.ImageField(blank=True,null=True,upload_to='organizacion/',default='organizacion/bandera_default.png')
    
    def save(self, force_insert=False, force_update=False):
        self.nombre_oficial= self.nombre_oficial.upper()
        self.siglas= self.siglas.upper()
        self.descripcion= self.descripcion.upper()
        super(organizacion, self).save(force_insert, force_update)

    def __str__(self):
        return str(self.nombre_oficial)

    class Meta:
        verbose_name_plural='organizaciones'
class jornada(models.Model):
    jornada_id=models.BigAutoField(primary_key=True)
    nombre=models.CharField(max_length=30)
    
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(jornada, self).save(force_insert, force_update)

    def __str__(self):
        return str(self.nombre)
    
    class Meta: 
        verbose_name_plural='jornada'
                
class competicion(models.Model):
    competicion_id=models.BigAutoField(primary_key=True)
    organizacion_id=models.ForeignKey(organizacion,on_delete=models.CASCADE, db_column='organizacion_id', null=True)
    logo_competicion=models.ImageField(null=True,blank=True,upload_to='competicion/logo/',default='competicion/logo/logo_default.png')
    nombre=models.CharField(max_length=50)
    pais_id=models.ForeignKey(pais,on_delete=models.CASCADE, db_column='pais_id',null=True,blank=True,)
    jornadas=models.IntegerField(db_column='jornada',blank=True,null=True)
    estado=models.BooleanField()
    fecha_inicio=models.DateField(blank=True,null=True,default='1990-12-12')
    fecha_fin=models.DateField(blank=True,null=True,default='1990-12-12')

    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(competicion, self).save(force_insert, force_update)

    def __str__(self):
         return str(self.nombre)
    
    class Meta:
        verbose_name_plural='competicion'

class detalle_patrocinador(models.Model):
    patrocinador_id=models.ForeignKey(patrocinador,on_delete=models.CASCADE, db_column='patrocinador_id')
    competicion_id=models.ForeignKey(competicion,on_delete=models.CASCADE, db_column='competicion_id')
    
    def __str__(self):
         return str(self.competicion_id)
    
    class Meta:
        verbose_name_plural='Patrocinador_Competicion'

class grupo(models.Model):
    grupo_id=models.BigAutoField(primary_key=True)
    nombre=models.CharField(max_length=30)
    
    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(grupo, self).save(force_insert, force_update)

    def __str__(self):
        return str(self.nombre)
    
    class Meta: 
        verbose_name_plural='grupo'
        


class fase(models.Model):
    fase_id=models.BigAutoField(primary_key=True)
    nombre=models.CharField(max_length=50)

    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        super(fase,self).save(force_insert, force_update)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural='fase'


class detalle_grupo(models.Model):
    detalle_grupo_id=models.BigAutoField(primary_key=True)
    equipo_id=models.ForeignKey("appEquipo.equipo",on_delete=models.CASCADE, db_column='equipo_id')
    fase_id=models.ForeignKey(fase,on_delete=models.CASCADE, db_column='fase_id')
    grupo_id=models.ForeignKey(grupo,on_delete=models.CASCADE, db_column='grupo_id')
    competicion_id=models.ForeignKey(competicion,on_delete=models.CASCADE, db_column='competicion_id')

    def __str__(self):
        return str(self.fase_id)
    
    class Meta: 
        verbose_name_plural='Grupo_competicion'

class tabla_posicion(models.Model):
    tabla_id=models.BigAutoField(primary_key=True)
    competicion_id=models.ForeignKey(competicion,on_delete=models.CASCADE, db_column='competicion_id')
    equipo_id=models.ForeignKey("appEquipo.equipo",on_delete=models.CASCADE, db_column='equipo_id')
    ganado=models.IntegerField()
    perdido=models.IntegerField()
    empatado=models.IntegerField()
    goles_favor=models.IntegerField()
    goles_contra=models.IntegerField()
    tarjetas_amarillas=models.IntegerField()
    tarjetas_rojas=models.IntegerField()
    puntos=models.IntegerField()

    def __str__(self):
        return str(self.competicion_id)
    
    class Meta: 
        verbose_name_plural='tabla_posicion'
        