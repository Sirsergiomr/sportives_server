# Generated by Django 2.2.3 on 2021-04-28 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0020_auto_20210428_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrenamiento',
            name='fecha',
            field=models.DateTimeField(),
        ),
    ]
