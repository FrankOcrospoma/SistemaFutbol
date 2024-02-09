# Generated by Django 4.1.1 on 2024-01-13 02:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appCompeticion', '0019_competicion_jornadas'),
        ('appPartido', '0043_alter_encuentro_competicion_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuentro',
            name='competicion_id',
            field=models.ForeignKey(db_column='competicion', on_delete=django.db.models.deletion.CASCADE, related_name='Competicion', to='appCompeticion.competicion'),
        ),
    ]
