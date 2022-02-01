# Generated by Django 4.0.1 on 2022-01-30 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_django', '0017_rename_alert_camera_red_zone_red_zone_camera_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='identificador',
            field=models.CharField(default=1643576816802, max_length=255),
        ),
        migrations.AlterField(
            model_name='alert',
            name='slug',
            field=models.SlugField(default='alerta_1643576816802'),
        ),
        migrations.AlterField(
            model_name='alert',
            name='timestamp',
            field=models.IntegerField(default=1643576816),
        ),
        migrations.AlterField(
            model_name='red_zone',
            name='dots_txt',
            field=models.FileField(upload_to='uploads/red_zones/<django.db.models.query_utils.DeferredAttribute object at 0x7fa11cbd5b80>'),
        ),
        migrations.AlterField(
            model_name='red_zone',
            name='identificador',
            field=models.CharField(default=1643576816803, max_length=255),
        ),
        migrations.AlterField(
            model_name='red_zone',
            name='slug',
            field=models.SlugField(default='red_zone_<django.db.models.query_utils.DeferredAttribute object at 0x7fa11cbd5b80>_1643576816803'),
        ),
        migrations.AlterField(
            model_name='red_zone',
            name='timestamp',
            field=models.IntegerField(default=1643576816),
        ),
        migrations.CreateModel(
            name='condensed_red_zones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificador', models.CharField(default=1643576816804, max_length=255)),
                ('slug', models.SlugField(default='condensed_red_zones_<django.db.models.query_utils.DeferredAttribute object at 0x7fa11cbd5b80>_1643576816')),
                ('timestamp', models.IntegerField(default=1643576816)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(default='example', max_length=255)),
                ('red_zones_txt', models.FileField(upload_to='uploads/red_zones/<django.db.models.query_utils.DeferredAttribute object at 0x7fa11cbd5b80>/condensed')),
                ('conteudo', models.TextField(default='nome: example, largura: 1980, altura: 1080, pontos: 574.84375,240.5625,587.84375,368.5625,676.84375,369.5625,614.84375,266.5625,')),
                ('local_dots_url', models.TextField(default='uploads/red_zones/None/red_zones_ex.txt')),
                ('red_zone_camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='this_camera_red_zones', to='app_django.camera')),
            ],
            options={
                'ordering': ('-date_added',),
            },
        ),
    ]