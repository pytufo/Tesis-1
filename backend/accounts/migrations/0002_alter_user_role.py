# Generated by Django 4.1.3 on 2023-11-21 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Administrator'), (2, 'Biblotecario'), (3, 'Profesor'), (4, 'Tesorero'), (5, 'Alumno'), (6, 'Invitado')], default=6, null=True),
        ),
    ]
