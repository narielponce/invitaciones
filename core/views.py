# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, ConfirmacionAsistencia, CancionPlaylist
import datetime
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO

def home_cliente(request, slug):
    cliente = get_object_or_404(Cliente, slug=slug)

    event_datetime_iso_string = None

    if cliente.fecha_evento and cliente.hora_evento:
        naive_dt = datetime.datetime.combine(cliente.fecha_evento, cliente.hora_evento)
        event_datetime_aware = timezone.make_aware(naive_dt, timezone.get_current_timezone())
        event_datetime_iso_string = event_datetime_aware.isoformat()
        print(event_datetime_iso_string)

    context = {
        'cliente': cliente,
        'event_datetime_iso_string': event_datetime_iso_string,
    }
    print(context)
    # Selección dinámica del template
    template_slug = cliente.template.slug if getattr(cliente, "template", None) and cliente.template else 'clasica'
    template_name = f"core/plantillas/{template_slug}/index.html"
    print (template_name)

    # Fallback a la plantilla clásica si no existe la seleccionada
    from django.template import TemplateDoesNotExist
    try:
        return render(request, template_name, context)
    except TemplateDoesNotExist:
        return render(request, "core/plantillas/clasica/index.html", context)


def panel_confirmaciones(request, tipo_evento, slug):
    token = request.GET.get('token')
    cliente = get_object_or_404(Cliente, slug=slug)
    
    # Verificar que el tipo_evento coincida con el cliente
    if cliente.get_url_prefix() != tipo_evento:
        return render(request, 'core/acceso_denegado.html', status=404)
    
    if not token or token != cliente.token_acceso:
        return render(request, 'core/acceso_denegado.html', status=403)
    
    confirmaciones = cliente.confirmaciones.all()
    return render(request, 'core/panel_confirmaciones.html', {
        'cliente': cliente,
        'confirmaciones': confirmaciones,
    })


def rsvp(request, slug):
    cliente = get_object_or_404(Cliente, slug=slug)
    if request.method == "POST":
        nombre = request.POST.get("name")
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        #telefono_envio_confirmacion = request.POST.get("telefono_envio_confirmacion")
        asistencia = request.POST.get("attendance") == "yes"
        cantidad = int(request.POST.get("guests", 0))
        restricciones = request.POST.get("dietary_restrictions", "")
        ConfirmacionAsistencia.objects.create(
            cliente=cliente,
            nombre_invitado=nombre,
            email=email,
            telefono=telefono,
            #telefono_envio_confirmacion=telefono_envio_confirmacion,
            asistencia=asistencia,
            cantidad_acompanantes=cantidad,
            restricciones_alimentarias=restricciones,
        )
        return render(request, "core/rsvp_gracias.html", {"cliente": cliente})
    # Si GET, solo renderiza la invitación normalmente (o redirige)
    return redirect("nombre_de_tu_vista_invitacion", slug=slug)


def exportar_excel(request, tipo_evento, slug):
    token = request.GET.get('token')
    cliente = get_object_or_404(Cliente, slug=slug)
    if cliente.get_url_prefix() != tipo_evento:
        return render(request, 'core/acceso_denegado.html', status=404)
    
    if not token or token != cliente.token_acceso:
        return render(request, 'core/acceso_denegado.html', status=403)
    
    confirmaciones = cliente.confirmaciones.all()
    
    # Crear workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Confirmaciones"
    
    # Headers
    headers = ['Nombre', 'Email', 'Teléfono', 'Asistencia', 'Acompañantes', 'Restricciones', 'Fecha']
    ws.append(headers)
    
    # Datos
    for c in confirmaciones:
        ws.append([
            c.nombre_invitado,
            c.email or '-',
            c.telefono or '-',
            'Sí' if c.asistencia else 'No',
            c.cantidad_acompanantes,
            c.restricciones_alimentarias or '-',
            c.fecha_confirmacion.strftime('%d/%m/%Y %H:%M')
        ])
    
    # Crear respuesta
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="confirmaciones_{cliente.slug}.xlsx"'
    
    wb.save(response)
    return response


def exportar_pdf(request, tipo_evento, slug):
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    from reportlab.lib import colors
    from io import BytesIO

    token = request.GET.get('token')
    cliente = get_object_or_404(Cliente, slug=slug)
    if cliente.get_url_prefix() != tipo_evento:
        return render(request, 'core/acceso_denegado.html', status=404)
    
    if not token or token != cliente.token_acceso:
        return render(request, 'core/acceso_denegado.html', status=403)

    confirmaciones = cliente.confirmaciones.all()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)
    elements = []

    # Datos para la tabla
    data = [['Nombre', 'Email', 'Teléfono', 'Asistencia', 'Acompañantes', 'Restricciones', 'Fecha']]
    for c in confirmaciones:
        data.append([
            c.nombre_invitado,
            c.email or '-',
            c.telefono or '-',
            'Sí' if c.asistencia else 'No',
            str(c.cantidad_acompanantes),
            c.restricciones_alimentarias or '-',
            c.fecha_confirmacion.strftime('%d/%m/%Y %H:%M')
        ])

    # Ajusta el ancho de columnas (en puntos, suma <= 540 para A4 vertical)
    col_widths = [70, 90, 60, 50, 50, 90, 70]

    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),  # Cabecera
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),  # Cuerpo
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]))

    elements.append(table)
    doc.build(elements)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="confirmaciones_{cliente.slug}.pdf"'
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def sugerir_cancion(request, slug):
    cliente = get_object_or_404(Cliente, slug=slug)
    if request.method == "POST":
        nombre_interprete = request.POST.get("nombre_interprete")
        nombre_tema = request.POST.get("nombre_tema")
        
        CancionPlaylist.objects.create(
            cliente=cliente,
            nombre_interprete=nombre_interprete,
            nombre_tema=nombre_tema,
        )
        return render(request, "core/playlist_gracias.html", {"cliente": cliente})
    
    return redirect("home_cliente", slug=slug)


def panel_canciones(request, tipo_evento, slug):
    token = request.GET.get('token')
    cliente = get_object_or_404(Cliente, slug=slug)
    
    # Verificar que el tipo_evento coincida con el cliente
    if cliente.get_url_prefix() != tipo_evento:
        return render(request, 'core/acceso_denegado.html', status=404)
    
    if not token or token != cliente.token_acceso:
        return render(request, 'core/acceso_denegado.html', status=403)
    
    canciones = cliente.canciones.all()
    return render(request, 'core/panel_canciones.html', {
        'cliente': cliente,
        'canciones': canciones,
    })


def exportar_excel_canciones(request, tipo_evento, slug):
    token = request.GET.get('token')
    cliente = get_object_or_404(Cliente, slug=slug)
    if cliente.get_url_prefix() != tipo_evento:
        return render(request, 'core/acceso_denegado.html', status=404)
    if not token or token != cliente.token_acceso:
        return render(request, 'core/acceso_denegado.html', status=403)
    canciones = cliente.canciones.all()
    wb = Workbook()
    ws = wb.active
    ws.title = "Canciones"
    headers = ['Intérprete', 'Tema', 'Fecha sugerencia']
    ws.append(headers)
    for c in canciones:
        ws.append([
            c.nombre_interprete,
            c.nombre_tema,
            c.fecha_sugerencia.strftime('%d/%m/%Y %H:%M')
        ])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="canciones_{cliente.slug}.xlsx"'
    wb.save(response)
    return response


def exportar_pdf_canciones(request, tipo_evento, slug):
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    from reportlab.lib import colors
    from io import BytesIO
    token = request.GET.get('token')
    cliente = get_object_or_404(Cliente, slug=slug)
    if cliente.get_url_prefix() != tipo_evento:
        return render(request, 'core/acceso_denegado.html', status=404)
    if not token or token != cliente.token_acceso:
        return render(request, 'core/acceso_denegado.html', status=403)
    canciones = cliente.canciones.all()
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)
    elements = []
    data = [['Intérprete', 'Tema', 'Fecha sugerencia']]
    for c in canciones:
        data.append([
            c.nombre_interprete,
            c.nombre_tema,
            c.fecha_sugerencia.strftime('%d/%m/%Y %H:%M')
        ])
    col_widths = [120, 220, 120]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]))
    elements.append(table)
    doc.build(elements)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="canciones_{cliente.slug}.pdf"'
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

from django.shortcuts import render

def landing(request):
    return render(request, 'core/index.html')