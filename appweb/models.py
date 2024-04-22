from django.db import models
from .models import *
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from uuid import uuid4
import os
from django.utils import encoding
import re
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def path_and_rename(instance, filename):
    upload_to = 'Mecanico/'
    ext = filename.split('.')[-1]
    
    # Si instance.nombre es None, genera un nombre de archivo aleatorio
    if instance.nombre:
        filename = '{}.{}'.format(instance.nombre, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    
    # Asegúrate de devolver el nombre del archivo modificado
    return os.path.join(upload_to, filename)


class Mecanico(models.Model):
    rut = models.CharField(max_length=70, default='1-0')
    nombre = models.CharField(max_length=70)
    edad = models.IntegerField(default=0)
    apellido = models.CharField(max_length=80)
    email = models.EmailField(default='example@example.com')
    especialista = models.CharField(max_length=100, default='Sin especialidad')
    fecha_nacimiento = models.DateField()
    foto = models.ImageField(upload_to=path_and_rename, null=True)
    descripcion = models.CharField(max_length=80, default='0')

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('detalle_mecanico', kwargs={'pk': self.pk})

class Trabajo(models.Model):
    CATEGORIAS_CHOICES = [
        ('Mantencion', 'Mantencion'),
        ('Reparacion', 'Reparacion'),
        ('Diagnostico', 'Diagnostico'),
    ]

    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    mecanico = models.ForeignKey(Mecanico, on_delete=models.CASCADE)
    imagenes = models.ImageField(upload_to="Trabajos/", null=True)
    autorizado = models.BooleanField(default=False)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS_CHOICES, default="Mantencion")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.titulo

class Administrador(models.Model):
    nombre = models.CharField(max_length=10)
    apellido = models.CharField(max_length=80)        
    fecha = models.DateField()
    motivo_rechazo = models.TextField(blank=True)

   


tipos_contacto = [
    [0, "Sugerencia"],
    [1, "Reclamo"]
]


    
def validate_integer(value):
    try:
        int(value)
    except ValueError:
        raise ValidationError(_('Debes ingresar solo numeros!'))

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField(validators=[EmailValidator(message="Ingrese una dirección de correo electrónico válida. ej: ejemplo@ejemplo.com")], default="@")
    telefono = models.CharField(max_length=12, validators=[MinLengthValidator(limit_value=12, message="Ingrese un numero Valído."), validate_integer], help_text="Ingrese número de teléfono válido.\n Nos pondremos en contacto con usted.\n  GarajelosHermanos.cl", default="+569")
    tipo_contacto = models.IntegerField(choices=tipos_contacto)
    mensaje = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Administrar Contacto de clientes web"
       
    def __str__(self):
        tipo_contacto_str = dict(tipos_contacto)[self.tipo_contacto]
        return f"Contacto: {self.nombre} ({self.email}) - Tipo de Contacto: {tipo_contacto_str}"

    def get_absolute_url(self):
        return reverse('contacto')


    
class Imagen(models.Model):
    imagen = models.ImageField(upload_to="Trabajos/")
    # Puedes agregar campos adicionales según tus necesidades, como título, descripción, etc.

    def __str__(self):
        return self.imagen.name
    

class Curriculum(models.Model):
    nombre = models.CharField(max_length=70)
    segundo_nombre= models.CharField(max_length=70)
    apellido = models.CharField(max_length=70)
    segundo_apellido = models.CharField(max_length=70)
    rut = models.CharField(max_length=70, default='1-0')
    fecha_nacimiento = models.DateField(null=True)
    numero_telefono = models.IntegerField(null=True)    
    email = models.EmailField(validators=[EmailValidator(message="Ingrese una dirección de correo electrónico válida.")], default="@")
    foto = models.ImageField(upload_to="Curriculums/", null=True)
    experiencia = models.TextField(max_length=2000)
    especialidad = models.CharField(max_length=30, null=True)


    

def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]', '', text)

def path_and_rename(instance, filename):
    upload_to = 'publicidad/'  # Cambia 'publicidad/' por la ruta deseada
    ext = filename.split('.')[-1]
    
    if instance.descripcion:
        # Limpiar el texto para eliminar caracteres no ASCII
        safe_filename = remove_non_ascii(instance.descripcion)
        filename = '{}.{}'.format(safe_filename, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    
    return os.path.join(upload_to, filename)

class Publicidad(models.Model):
    imagen = models.ImageField(upload_to=path_and_rename)
    descripcion = models.TextField()
    enlace = models.URLField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    prioridad = models.PositiveIntegerField(default=0)
    max_ancho = models.PositiveIntegerField(default=0, help_text='Ancho máximo en píxeles para la imagen')
    max_alto = models.PositiveIntegerField(default=0, help_text='Alto máximo en píxeles para la imagen')

    def __str__(self):
        return self.descripcion
        
    class Meta:
        verbose_name_plural = "Administrar Imágenes Home/Principal"
        
    def get_absolute_url(self):
        # Redirecciona al usuario a la página de inicio
        return reverse('home')  # Ajusta 'home' al nombre de tu vista de página de inicio

def validate_integer(value):
    try:
        int(value)
    except ValueError:
        raise ValidationError('Debes ingresar solo numeros!')

class Reserva(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    correo_usuario = models.EmailField(validators=[EmailValidator(message="Ingrese una dirección de correo electrónico válida. ej: ejemplo@ejemplo.com")])
    nombre_cliente = models.CharField(max_length=100)
    apellido_cliente = models.CharField(max_length=100)
    telefono_cliente = models.CharField(
        max_length=12,
        validators=[
            MinLengthValidator(limit_value=12, message="Ingrese un numero válido."),
            validate_integer,
        ],
        help_text="Ingrese número de teléfono válido. \n Nos pondremos en contacto con usted. \n GarajelosHermanos.cl",
        default="+569"
    )
    tipo_vehiculo = models.CharField(max_length=20, choices=[('auto', 'Auto'), ('moto', 'Moto')])
    marca_vehiculo = models.CharField(max_length=50)
    modelo_vehiculo = models.CharField(max_length=50)
    informacion_adicional = models.CharField(max_length=500, default="")

    class Meta:
        verbose_name_plural = "Administrar Reservas"
        
    def __str__(self):
        return f"Numero: {self.id} - Fecha: {self.fecha} - Hora: {self.hora}"

    def get_absolute_url(self):
        return reverse('reservas')


    ##SERVICIOS DEL TALLER

class Restauracion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen_antes = models.ImageField(upload_to='restauraciones/antes/')
    imagen_despues = models.ImageField(upload_to='restauraciones/despues/')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
        
    def get_absolute_url(self):
        return reverse('restauracion') 
        
    class Meta:
        verbose_name_plural = "Administrar Fotos Servicio de Restauración"

class Motos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='servicio_motos')    
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Administrar Fotos Servicio de Motos"

    def __str__(self):
        return self.nombre
        
    def get_absolute_url(self):
        return reverse('mecanica_motos')
        
class Pintura(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen_antes = models.ImageField(upload_to='servicio_pintura', default='ruta/a/tu/imagen_default_antes.jpg')
    imagen_despues = models.ImageField(upload_to='servicio_pintura', default='ruta/a/tu/imagen_default_despues.jpg')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('pintura_automotriz')
    
    class Meta:
        verbose_name_plural = "Administrar Fotos Servicio de Pintura"

    def __str__(self):
        return self.nombre


    
class Automotriz(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='servicio_autos')    
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Administrar Fotos Servicio Automotriz"
        
    def get_absolute_url(self):
        return reverse('mecanica_autos')

