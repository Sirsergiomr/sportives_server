# Generated by Django 2.2.3 on 2021-05-24 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0030_entrenamiento_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='anuncio',
            name='pagado',
            field=models.BooleanField(default=False),
        ),
    ]
