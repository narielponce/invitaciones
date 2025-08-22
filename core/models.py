# core/models.py

import os
import uuid
from io import BytesIO
from PIL import Image

from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


def procesar_imagen(imagen_campo, max_size=800):
    """
    Recibe un ImageFieldFile, redimensiona y convierte a webp.
    Devuelve nuevo ContentFile para reemplazar.
    """
    if not imagen_campo:
        return None

    try:
        img = Image.open(imagen_campo)
        img.convert('RGB')  # Por si viene con transparencia

        # Resize si supera max_size
        if img.height > max_size or img.width > max_size:
            img.thumbnail((max_size, max_size))

        buffer = BytesIO()
        img.save(buffer, format='WEBP', quality=85)
        buffer.seek(0)

        webp_name = os.path.splitext(imagen_campo.name)[0] + '.webp'
        return webp_name, ContentFile(buffer.read())

    except Exception as e:
        print(f"Error procesando imagen: {e}")
        return None

GOOGLE_FONTS_CHOICES = [
    ('Great Vibes', 'Great Vibes'),
    ('Dancing Script', 'Dancing Script'),
    ('Allura', 'Allura'),
    ('Sacramento', 'Sacramento'),
    ('Parisienne', 'Parisienne'),
]

class Cliente(models.Model):
    TIPO_EVENTO_CHOICES = [
        ('15', 'Fiesta de 15'),
        ('boda', 'Casamiento'),
        ('cumple', 'Cumpleaños'),
        ('otros', 'Otros'),
    ]

    nombre = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    template = models.ForeignKey('Template', on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    telefono_envio_confirmacion = models.CharField(max_length=30, blank=True, null=True)
    tipo_evento = models.CharField(max_length=20, choices=TIPO_EVENTO_CHOICES)
    fecha_evento = models.DateField()
    
    fuente_nombre = models.CharField(max_length=50, choices=GOOGLE_FONTS_CHOICES, default='Great Vibes')
    mensaje_bienvenida = models.TextField(blank=True)
    hora_evento = models.TimeField()
    lugar_evento = models.CharField(max_length=255, blank=True)
    direccion_evento = models.TextField(blank=True)
    codigo_vestimenta = models.CharField(max_length=100, blank=True)
    
    instagram_url = models.URLField(max_length=300, blank=True, null=True)
    alias_regalos = models.CharField(max_length=100, blank=True)
    token_acceso = models.CharField(max_length=40, unique=True, blank=True, null=True)

    # Imágenes
    imagen_fondo = models.ImageField(upload_to='fondos/', blank=True, null=True)
    imagen_fondo_ig = models.ImageField(upload_to='fondos/', blank=True, null=True)
    
    imagen1 = models.ImageField(upload_to='galeria/', blank=True, null=True)
    imagen2 = models.ImageField(upload_to='galeria/', blank=True, null=True)
    imagen3 = models.ImageField(upload_to='galeria/', blank=True, null=True)
    imagen4 = models.ImageField(upload_to='galeria/', blank=True, null=True)
    imagen5 = models.ImageField(upload_to='galeria/', blank=True, null=True)
    imagen6 = models.ImageField(upload_to='galeria/', blank=True, null=True)
    imagen7 = models.ImageField(upload_to='galeria/', blank=True, null=True)
    imagen8 = models.ImageField(upload_to='galeria/', blank=True, null=True)
    imagen9 = models.ImageField(upload_to='galeria/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Crear slug/token si no existen
        if not self.slug:
            self.slug = slugify(self.nombre)
        if not self.token_acceso:
            self.token_acceso = uuid.uuid4().hex

        # Guardar primero para obtener paths
        super().save(*args, **kwargs)

        # Lista de campos a procesar
        imagenes_a_procesar = [
            'imagen_fondo',
            'imagen_fondo_ig',
            'imagen1', 'imagen2', 'imagen3', 'imagen4', 'imagen5',
            'imagen6', 'imagen7', 'imagen8', 'imagen9'
        ]

        actualizacion = False

        for campo in imagenes_a_procesar:
            imagen_campo = getattr(self, campo)
            if imagen_campo and not imagen_campo.name.endswith('.webp'):
                resultado = procesar_imagen(imagen_campo)
                if resultado:
                    nombre_webp, nuevo_archivo = resultado
                    getattr(self, campo).save(nombre_webp, nuevo_archivo, save=False)
                    actualizacion = True

        if actualizacion:
            super().save(update_fields=imagenes_a_procesar)

    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_evento_display()}"

    def get_url_prefix(self) -> str:
        mapping = {
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
            self.imagen1, self.imagen2, self.imagen3, self.imagen4,
            self.imagen5, self.imagen6, self.imagen7, self.imagen8,
            self.imagen9,
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

class Template(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=50)
    descripcion = models.TextField(blank=True)
    preview = models.ImageField(upload_to='previews/', blank=True, null=True)  # Opcional

    def __str__(self):
        return self.nombre