# invitaciones/urls.py
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from core import views as core_views
from django.conf.urls.static import static
from django.shortcuts import get_object_or_404
from core.models import Cliente
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('<slug:cliente_slug>/', core_views.home_cliente, name='home_cliente'),

    path('', core_views.landing, name='landing'),

    # URLs específicas por tipo de evento
    path('quince/<slug:slug>/', core_views.home_cliente, name='invitacion-quince'),
    path('boda/<slug:slug>/', core_views.home_cliente, name='invitacion-boda'),
    path('cumple/<slug:slug>/', core_views.home_cliente, name='invitacion-cumple'),
    path('varios/<slug:slug>/', core_views.home_cliente, name='invitacion-varios'),
    path('infantil/<slug:slug>/', core_views.home_cliente, name='invitacion-infantil'),

    # --- NUEVA RUTA PARA PROBAR EL REFACTOR ---
    path('v2/quince/<slug:slug>/', core_views.home_cliente_unificado, name='home_cliente_unificado'),

    # path('confirmaciones/<slug:slug>/', core_views.panel_confirmaciones, name='panel_confirmaciones'),
    path('<str:tipo_evento>/<slug:slug>/confirmaciones/', core_views.panel_confirmaciones, name='panel_confirmaciones'),
    path('<str:tipo_evento>/<slug:slug>/', core_views.home_cliente, name='home_cliente_original'),
    path('rsvp/<slug:slug>/', core_views.rsvp, name='rsvp'),

    # path('confirmaciones/<slug:slug>/excel/', core_views.exportar_excel, name='exportar_excel'),
    # path('confirmaciones/<slug:slug>/pdf/', core_views.exportar_pdf, name='exportar_pdf'),
    path('<str:tipo_evento>/<slug:slug>/confirmaciones/excel/', core_views.exportar_excel, name='exportar_excel'),
    path('<str:tipo_evento>/<slug:slug>/confirmaciones/pdf/', core_views.exportar_pdf, name='exportar_pdf'),

    path('playlist/<slug:slug>/', core_views.sugerir_cancion, name='sugerir_cancion'),
    path('<str:tipo_evento>/<slug:slug>/canciones/', core_views.panel_canciones, name='panel_canciones'),
    path('<str:tipo_evento>/<slug:slug>/canciones/excel/', core_views.exportar_excel_canciones, name='exportar_excel_canciones'),
    path('<str:tipo_evento>/<slug:slug>/canciones/pdf/', core_views.exportar_pdf_canciones, name='exportar_pdf_canciones'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
