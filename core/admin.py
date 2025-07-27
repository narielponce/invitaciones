# core/admin.py
from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "tipo_evento", "fecha_evento")
    prepopulated_fields = {"slug": ("nombre",)}
