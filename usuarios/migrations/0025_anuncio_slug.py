# Generated by Django 2.2.3 on 2021-05-01 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0024_anuncio'),
    ]

    operations = [
        migrations.AddField(
            model_name='anuncio',
            name='slug',
            field=models.SlugField(default=None, editable=False),
            preserve_default=False,
        ),
    ]
