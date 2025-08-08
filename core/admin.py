# core/admin.py
from django.contrib import admin
from .models import Cliente, ConfirmacionAsistencia, CancionPlaylist, Template

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "tipo_evento", "fecha_evento")
    list_filter = ("tipo_evento", "fecha_evento")
    search_fields = ("nombre", "titulo")
    prepopulated_fields = {"slug": ("nombre",)}
    list_per_page = 20
    ordering = ("-fecha_evento",)
    fieldsets = (
        (None, {
            'fields': ('nombre', 'titulo', 'slug', 'mensaje_bienvenida', 'template', 'fuente_nombre')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono_envio_confirmacion')
        }),
        ('Evento', {
            'fields': ('tipo_evento', 'lugar_evento', 'direccion_evento', 'fecha_evento', 'hora_evento')
        }),
        ('Otros', {
            'fields': ('codigo_vestimenta', 'instagram_url', 'alias_regalos', 'token_acceso')
        }),
        ('Imagenes', {
            'fields': (
                'imagen_fondo', 'imagen_fondo_ig', 'imagen1', 'imagen2', 'imagen3', 'imagen4',
                'imagen5', 'imagen6', 'imagen7', 'imagen8', 'imagen9'
            )
        }),
    )

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'descripcion')
    prepopulated_fields = {"slug": ("nombre",)}
