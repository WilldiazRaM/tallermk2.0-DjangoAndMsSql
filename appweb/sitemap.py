from django.contrib.sitemaps import Sitemap
from .models import Mecanico, Contacto, Publicidad, Reserva, Restauracion, Motos, Pintura, Automotriz
from django.urls import reverse


class FaviconSitemap(Sitemap):
    priority = 0.1
    changefreq = 'monthly'

    def items(self):
        return ['favicon']

    def location(self, item):
        return reverse('favicon')



class MecanicoSitemap(Sitemap):
    changefreq = 'semanal'
    priority = 0.9

    def items(self):
        return Mecanico.objects.all()

    def lastmod(self, obj):
        return obj.fecha_nacimiento


class ContactoSitemap(Sitemap):
    changefreq = 'mensual'
    priority = 0.7

    def items(self):
        return Contacto.objects.all()

    def lastmod(self, obj):
        return obj.fecha

class PublicidadSitemap(Sitemap):
    changefreq = 'diario'
    priority = 0.6

    def items(self):
        return Publicidad.objects.all()

    def lastmod(self, obj):
        return obj.fecha_inicio

class ReservaSitemap(Sitemap):
    changefreq = 'mensual'
    priority = 0.7

    def items(self):
        return Reserva.objects.all()

    def lastmod(self, obj):
        return obj.fecha

class RestauracionSitemap(Sitemap):
    changefreq = 'mensual'
    priority = 0.8

    def items(self):
        return Restauracion.objects.all()

    def lastmod(self, obj):
        return obj.fecha_publicacion

class MotosSitemap(Sitemap):
    changefreq = 'mensual'
    priority = 0.8

    def items(self):
        return Motos.objects.all()

    def lastmod(self, obj):
        return obj.fecha_publicacion

class PinturaSitemap(Sitemap):
    changefreq = 'mensual'
    priority = 0.8

    def items(self):
        return Pintura.objects.all()

    def lastmod(self, obj):
        return obj.fecha_publicacion

class AutomotrizSitemap(Sitemap):
    changefreq = 'mensual'
    priority = 0.8

    def items(self):
        return Automotriz.objects.all()

    def lastmod(self, obj):
        return obj.fecha_publicacion

# Registra tus sitemaps en el sitemap index
sitemaps = {
    'mecanico': MecanicoSitemap,
    'contacto': ContactoSitemap,
    'publicidad': PublicidadSitemap,
    'reserva': ReservaSitemap,
    'restauracion': RestauracionSitemap,
    'motos': MotosSitemap,
    'pintura': PinturaSitemap,
    'automotriz': AutomotrizSitemap,
    'favicon' : FaviconSitemap
    
}
