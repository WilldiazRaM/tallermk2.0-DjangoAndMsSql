from django.contrib import admin
from .models import *

#register you models here:
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email']
    list_editable = ['email']
    search_fields = ['nombre', 'email']



class AdministradorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'cargo', 'fecha']
    search_fields = ['nombre', 'apellido']
    list_filter = ['cargo']


class PublicidadAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'enlace', 'fecha_inicio', 'fecha_fin', 'prioridad')
    search_fields = ('descripcion',)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'marca', 'categoria', 'descripcion', 'precio', 'imagen_producto')
    search_fields = ('nombre', 'marca__nombre', 'categoria__nombre')


admin.site.register(Mecanico)
admin.site.register(Contacto) 
admin.site.register(Reserva)
admin.site.register(Publicidad)
admin.site.register(Restauracion)
admin.site.register(Pintura)
admin.site.register(Automotriz)
admin.site.register(Motos)
