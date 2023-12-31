# Generated by Django 4.0.7 on 2023-09-29 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_canton_detpersonapadronelectoral_eventoelectoral_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listaelectoral',
            name='logo_file',
            field=models.FileField(blank=True, default='', max_length=2000, null=True, upload_to='', verbose_name='Logo File'),
        ),
        migrations.AddField(
            model_name='listaelectoral',
            name='tipo',
            field=models.IntegerField(choices=[(1, 'Valido'), (2, 'Blanco'), (3, 'Nulo')], default=1, verbose_name='Tipo Voto'),
        ),
        migrations.AddField(
            model_name='votopersonapadron',
            name='tipo',
            field=models.IntegerField(choices=[(1, 'Valido'), (2, 'Blanco'), (3, 'Nulo')], default=1, verbose_name='Tipo Voto'),
        ),
    ]
