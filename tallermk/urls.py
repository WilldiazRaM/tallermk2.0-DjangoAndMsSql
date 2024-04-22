# urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from appweb.sitemap import sitemaps  # Ajusta la ruta según la ubicación real de tu archivo sitemap.py
from django.shortcuts import render
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('appweb.urls')),  # URL base de la aplicación appweb

    # Rutas más específicas
   
    path('contacto/', include('appweb.urls')),
    path('loginCliente/', include('appweb.urls')),
    path('loginMecanido/', include('appweb.urls')),
    path('loginAdmin/', include('appweb.urls')),
    path('galeriaMecanicos/', include('appweb.urls')),
    path('home/', include('appweb.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Configura el manejador de errores 404
handler404 = 'appweb.views.error_404'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
