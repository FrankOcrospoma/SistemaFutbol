# Generated by Django 4.1.1 on 2023-11-24 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appContrato', '0010_remove_contrato_tipo_persona'),
        ('appPartido', '0024_remove_evento_alineacion1_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='contrato_id1',
            field=models.ForeignKey(blank=True, db_column='contrato_id1', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eventos_contrato1', to='appContrato.contrato'),
        ),
        migrations.AddField(
            model_name='evento',
            name='contrato_id2',
            field=models.ForeignKey(blank=True, db_column='contrato_id2', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eventos_contrato2', to='appContrato.contrato'),
        ),
    ]