# core/models.py

from django.db import models
from django.utils.text import slugify
from typing import Literal
from django.urls import reverse
import uuid


class Cliente(models.Model):
    TIPO_EVENTO_CHOICES = [
        ('15', 'Fiesta de 15'),
        ('boda', 'Casamiento'),
        ('cumple', 'Cumpleaños'),
        ('otros', 'Otros'),
    ]

    nombre = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100, blank=False)
    slug = models.SlugField(unique=True, max_length=100)
    email = models.EmailField()
    telefono_envio_confirmacion = models.CharField(max_length=30, blank=True, null=True)
    tipo_evento = models.CharField(max_length=20, choices=TIPO_EVENTO_CHOICES)
    fecha_evento = models.DateField()

    mensaje_bienvenida = models.TextField(blank=True)
    hora_evento = models.TimeField(null=True, blank=True)
    lugar_evento = models.CharField(max_length=255, blank=True)
    direccion_evento = models.TextField(blank=True)
    codigo_vestimenta = models.CharField(max_length=100, blank=True)
    instagram_url = models.URLField(max_length=300, blank=True, null=True)
    alias_regalos = models.CharField(max_length=100, blank=True)
    token_acceso = models.CharField(max_length=40, unique=True, blank=True, null=True)

    imagen_fondo = models.ImageField(upload_to='fondos/', blank=True, null=True)
    
    # Galería (hasta 8 imágenes)
    imagen1 = models.ImageField(upload_to='galeria/', blank=True, null=True)
    imagen2 = models.ImageField(upload_to='galeria/', blank=True, null=True)
    imagen3 = models.ImageField(upload_to='galeria/', blank=True, null=True)
    imagen4 = models.ImageField(upload_to='galeria/', blank=True, null=True)
    imagen5 = models.ImageField(upload_to='galeria/', blank=True, null=True)
    imagen6 = models.ImageField(upload_to='galeria/', blank=True, null=True)
    imagen7 = models.ImageField(upload_to='galeria/', blank=True, null=True)
    imagen8 = models.ImageField(upload_to='galeria/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        if not self.token_acceso:
            self.token_acceso = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_evento_display()}"  # type: ignore[attr-defined]

    def get_url_prefix(self) -> str:
        mapping: dict[str, str] = {
            '15': 'quince',
            'boda': 'boda',
            'cumple': 'cumple',
            'otros': 'varios',
        }
        return mapping.get(str(self.tipo_evento)) or 'varios'

    def get_absolute_url(self):
        return reverse(f'invitacion-{self.get_url_prefix()}', kwargs={'slug': self.slug})

    @property
    def imagenes(self):
        return [
            self.imagen1,
            self.imagen2,
            self.imagen3,
            self.imagen4,
            self.imagen5,
            self.imagen6,
            self.imagen7,
            self.imagen8,
        ]


class ConfirmacionAsistencia(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='confirmaciones')
    nombre_invitado = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    asistencia = models.BooleanField()  # True=asiste, False=no asiste
    fecha_confirmacion = models.DateTimeField(auto_now_add=True)
    cantidad_acompanantes = models.PositiveIntegerField(default=1)  # type: ignore[arg-type]
    restricciones_alimentarias = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre_invitado} ({'Asiste' if self.asistencia else 'No asiste'})"


class CancionPlaylist(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='canciones')
    nombre_interprete = models.CharField(max_length=100)
    nombre_tema = models.CharField(max_length=200)
    fecha_sugerencia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_tema} - {self.nombre_interprete}"

    class Meta:
        ordering = ['-fecha_sugerencia']