# Generated by Django 2.2.3 on 2021-04-28 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0016_auto_20210428_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activiadad',
            name='fecha',
            field=models.DateField(),
        ),
    ]
