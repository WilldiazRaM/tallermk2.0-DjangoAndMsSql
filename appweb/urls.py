from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from .sitemap import sitemaps
from . import views
from django.views.generic.base import RedirectView




from .views import (
    home, eliminarCurriculum, listar_trabajo4Mecanico,
    contacto, galeriaMecanicos, agregar_mecanico, listar_mecanico,
    modificar_mecanico, eliminar_mecanico, login_usuario, registro_mecanico,
    agregar_trabajo, listar_trabajos, modificar_trabajo, autorizar_trabajo,
    rechazar_trabajo, trabaja_con_nosotros, listarTrabajoHome, listarCurriculums,
    verPostulacion, mecanica_autos, mecanica_motos, pintura_automotriz, restauracion,
    reserva_view, reserva_view, ConfirmacionView, detalle_mecanico
    
)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', home, name='home'),
    path('contacto/', contacto, name="contacto"),    
    path('galeriaMecanicos/', galeriaMecanicos, name="galeriaMecanicos"),
    path('Mantenedor/mecanico/agregar', agregar_mecanico, name="agregar_mecanico"),
    path('Mantenedor/mecanico/listar', listar_mecanico, name="listar_mecanico"),
    path('Mantenedor/mecanico/modificar/<rut>', modificar_mecanico, name="modificar_mecanico"),
    path('Mantenedor/mecanico/eliminar/<rut>', eliminar_mecanico, name="eliminar_mecanico"),
    path('login_usuario/', login_usuario, name="login_usuario"),
    path('registro_mecanico', registro_mecanico, name="registro_mecanico"),
    path('Mantenedor/Trabajo/agregar', agregar_trabajo, name="agregar_trabajo"),  
    path('Mantenedor/Trabajo/listar', listar_trabajos, name="listar_trabajo"),
    path('Mantenedor/Trabajo/listar/mecanico', listar_trabajo4Mecanico, name="listar_trabajo4Mecanico"),
    path('Mantenedor/Trabajo/modificar/<titulo>/', modificar_trabajo, name="modificar_trabajo"),
    path('Mantenedor/Trabajo/autorizar/<int:pk>/', autorizar_trabajo, name="autorizar_trabajo"),
    path('Mantenedor/Trabajo/rechazar/<int:pk>/', rechazar_trabajo, name="rechazar_trabajo"),
    path('Mantenedor/Trabajo/listarTrabajoHome/<str:titulo>/', listarTrabajoHome, name="listarTrabajosHome"),
    path('TrabajaConNosotros/', trabaja_con_nosotros , name="trabaja_con_nosotros"),
    path('Mantenedor/Curriculum/listarCurriculum', listarCurriculums , name="listarCurriculum"),
    path('Mantenedor/Curriculum/detallePostulacion/<pk>/' , verPostulacion, name="verPostulacion"),
    path('Mantenedor/Curriculum/eliminarPostulacion/<pk>/' , eliminarCurriculum, name="eliminarCurriculum"),
    path('reserva/', reserva_view, name="reservas"),
    path('Servicios/mecanica_autos/', mecanica_autos, name='mecanica_autos'),
    path('Servicios/mecanica_motos/', mecanica_motos, name='mecanica_motos'),
    path('Servicios/pintura_automotriz/', pintura_automotriz, name='pintura_automotriz'),
    path('Servicios/restauracion/', restauracion, name='restauracion'),
    path('confirmacion/<int:reserva_id>/', ConfirmacionView.as_view(), name='reservconfirmed'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('mecanico/<int:pk>/', views.detalle_mecanico, name='detalle_mecanico'),
    path('favicon.ico', RedirectView.as_view(url='/static/logoTallerICO.ico'), name='favicon')           
        ] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
