# Generated by Django 2.2.3 on 2021-04-24 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0008_entrenamiento_tiempo_uso'),
    ]

    operations = [
        migrations.AddField(
            model_name='activiadad',
            name='entrenamiento',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='usuarios.Entrenamiento'),
            preserve_default=False,
        ),
    ]