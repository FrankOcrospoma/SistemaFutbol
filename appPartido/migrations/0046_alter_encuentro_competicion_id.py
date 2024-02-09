# Generated by Django 4.1.1 on 2024-01-13 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appCompeticion', '0019_competicion_jornadas'),
        ('appPartido', '0045_alter_encuentro_competicion_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuentro',
            name='competicion_id',
            field=models.ForeignKey(db_column='competicion_id', on_delete=django.db.models.deletion.CASCADE, to='appCompeticion.competicion'),
        ),
    ]
