# Generated by Django 4.1.1 on 2023-11-22 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appCompeticion', '0012_alter_detalle_grupo_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organizacion',
            name='tipo',
        ),
        migrations.RemoveField(
            model_name='pais',
            name='estado',
        ),
    ]