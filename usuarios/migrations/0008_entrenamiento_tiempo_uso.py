# Generated by Django 2.2.3 on 2021-04-24 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_maquina_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrenamiento',
            name='tiempo_uso',
            field=models.TimeField(default='00:00:00'),
        ),
    ]
