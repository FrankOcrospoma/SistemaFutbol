# Generated by Django 4.1.1 on 2024-01-20 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appPartido', '0046_alter_encuentro_competicion_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='tiempo_extra',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]