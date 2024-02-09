# Generated by Django 4.1.1 on 2023-12-21 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appCompeticion', '0015_alter_organizacion_tipo'),
        ('appPartido', '0038_evento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuentro',
            name='grupo',
            field=models.ForeignKey(blank=True, db_column='grupo', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grupo', to='appCompeticion.grupo'),
        ),
    ]