# Generated by Django 4.1.1 on 2023-11-29 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appContrato', '0011_alter_persona_organizacion_id'),
        ('appEquipo', '0025_equipo_entrenador_id_tipo_equipo_estado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo',
            name='entrenador_id',
            field=models.ForeignKey(db_column='contrato_id', limit_choices_to={'persona__tipo_persona_id': 2}, null=True, on_delete=django.db.models.deletion.CASCADE, to='appContrato.contrato'),
        ),
    ]
