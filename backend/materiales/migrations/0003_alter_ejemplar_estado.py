# Generated by Django 4.1.3 on 2023-11-21 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0002_remove_reservas_articulo_remove_reservas_owner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ejemplar',
            name='estado',
            field=models.CharField(blank=True, choices=[('d', 'Disponible'), ('n', 'No disponible')], default='d', help_text='Estado de Ejemplar', max_length=1, null=True),
        ),
    ]
