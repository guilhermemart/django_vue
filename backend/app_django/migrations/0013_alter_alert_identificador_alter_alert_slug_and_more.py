# Generated by Django 4.0.1 on 2022-01-28 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_django', '0012_alter_alert_identificador_alter_alert_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='identificador',
            field=models.CharField(default=1643387460243, max_length=255),
        ),
        migrations.AlterField(
            model_name='alert',
            name='slug',
            field=models.SlugField(default='alerta_1643387460243'),
        ),
        migrations.AlterField(
            model_name='alert',
            name='timestamp',
            field=models.IntegerField(default=1643387460),
        ),
    ]
