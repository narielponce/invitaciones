# core/admin.py
from django.contrib import admin
from .models import Cliente, ConfirmacionAsistencia, CancionPlaylist, Template

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "tipo_evento", "fecha_evento")
    prepopulated_fields = {"slug": ("nombre",)}

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'descripcion')
    prepopulated_fields = {"slug": ("nombre",)}
