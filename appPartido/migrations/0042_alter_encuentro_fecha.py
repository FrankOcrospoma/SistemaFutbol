# Generated by Django 4.1.1 on 2024-01-13 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appPartido', '0041_alter_encuentro_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuentro',
            name='fecha',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
