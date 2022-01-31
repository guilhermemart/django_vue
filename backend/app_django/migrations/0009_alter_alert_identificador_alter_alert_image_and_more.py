# Generated by Django 4.0.1 on 2022-01-31 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_django', '0008_alter_alert_identificador_alter_alert_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='identificador',
            field=models.CharField(default=1643631981893, max_length=255),
        ),
        migrations.AlterField(
            model_name='alert',
            name='image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='uploads/sauron_imagens/n_avaliadas'),
        ),
        migrations.AlterField(
            model_name='alert',
            name='local_image_url',
            field=models.TextField(default='uploads/sauron_imagens/n_avaliadas/example.png'),
        ),
        migrations.AlterField(
            model_name='alert',
            name='slug',
            field=models.SlugField(default='alerta_1643631981893'),
        ),
        migrations.AlterField(
            model_name='alert',
            name='thumbnail',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='uploads/sauron_thumbnails/'),
        ),
        migrations.AlterField(
            model_name='alert',
            name='timestamp',
            field=models.IntegerField(default=1643631981),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(default='Nonconformity', max_length=255),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='Nonconformity'),
        ),
    ]