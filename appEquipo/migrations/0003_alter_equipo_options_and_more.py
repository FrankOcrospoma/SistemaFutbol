# Generated by Django 4.1.1 on 2023-11-02 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appEquipo', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipo',
            options={'verbose_name_plural': 'equipos'},
        ),
        migrations.RemoveField(
            model_name='equipo',
            name='vestimenta_alterna',
        ),
        migrations.RemoveField(
            model_name='equipo',
            name='vestimenta_principal',
        ),
        migrations.AddField(
            model_name='equipo',
            name='vestimenta_alterna_color_principal',
            field=models.CharField(default='#FFFFFF', max_length=7),
        ),
        migrations.AddField(
            model_name='equipo',
            name='vestimenta_alterna_color_secundario',
            field=models.CharField(default='#FFFFFF', max_length=7),
        ),
        migrations.AddField(
            model_name='equipo',
            name='vestimenta_principal_color_principal',
            field=models.CharField(default='#FFFFFF', max_length=7),
        ),
        migrations.AddField(
            model_name='equipo',
            name='vestimenta_principal_color_secundario',
            field=models.CharField(default='#FFFFFF', max_length=7),
        ),
    ]