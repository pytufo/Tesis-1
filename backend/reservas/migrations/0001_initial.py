# Generated by Django 4.1.3 on 2023-12-09 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('materiales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField(auto_now_add=True)),
                ('fecha_fin', models.DateField()),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material', to='materiales.material')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['fecha_fin'],
            },
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField(auto_now_add=True)),
                ('fecha_fin', models.DateField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Autor', to=settings.AUTH_USER_MODEL)),
                ('ejemplar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ejemplar', to='materiales.ejemplar')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Prestamos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['fecha_fin'],
            },
        ),
    ]
