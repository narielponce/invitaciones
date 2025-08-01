# Generated by Django 5.2.4 on 2025-07-24 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_cliente_imagen_fondo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='instagram_url',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='titulo',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='tipo_evento',
            field=models.CharField(choices=[('15', 'Fiesta de 15'), ('boda', 'Casamiento'), ('cumple', 'Cumpleaños')], max_length=20),
        ),
    ]
