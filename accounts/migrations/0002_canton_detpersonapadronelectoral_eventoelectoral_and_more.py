# Generated by Django 4.2.5 on 2023-09-26 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Canton",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nombre",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=1000,
                        null=True,
                        verbose_name="Nombre",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DetPersonaPadronElectoral",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "dni",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=1000,
                        null=True,
                        verbose_name="DNI",
                    ),
                ),
                (
                    "nombre",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=1000,
                        null=True,
                        verbose_name="Nombre",
                    ),
                ),
                (
                    "apellido",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=1000,
                        null=True,
                        verbose_name="Apellido",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EventoElectoral",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nombre",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=1000,
                        null=True,
                        verbose_name="Nombre",
                    ),
                ),
                (
                    "fecha",
                    models.DateField(
                        blank=True, null=True, verbose_name="Fecha Elección"
                    ),
                ),
            ],
            options={
                "verbose_name": "Padron Electoral",
                "verbose_name_plural": "Padron Electoral",
            },
        ),
        migrations.CreateModel(
            name="ListaElectoral",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nombre",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=1000,
                        null=True,
                        verbose_name="Nombre",
                    ),
                ),
                (
                    "logo",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=2000,
                        null=True,
                        verbose_name="Logo",
                    ),
                ),
                (
                    "cab",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.eventoelectoral",
                        verbose_name="Cab",
                    ),
                ),
            ],
            options={
                "verbose_name": "Lista Electoral",
                "verbose_name_plural": "Listas Electorales",
            },
        ),
        migrations.CreateModel(
            name="Provincia",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nombre",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=1000,
                        null=True,
                        verbose_name="Nombre",
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="customuser",
            name="documento",
            field=models.CharField(default="999999999", max_length=10, unique=True),
        ),
        migrations.CreateModel(
            name="VotoPersonaPadron",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "cab",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.eventoelectoral",
                        verbose_name="Cab",
                    ),
                ),
                (
                    "lista",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.listaelectoral",
                        verbose_name="Listas electorales",
                    ),
                ),
                (
                    "persona",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.detpersonapadronelectoral",
                        verbose_name="Persona",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TablaResultado",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "empadronado",
                    models.IntegerField(
                        default=0, verbose_name="Numero de empadronados"
                    ),
                ),
                (
                    "ausentismo",
                    models.IntegerField(
                        default=0, verbose_name="Votos no utilizados (ausentismo)"
                    ),
                ),
                (
                    "votovalido",
                    models.IntegerField(default=0, verbose_name="Votos total validos"),
                ),
                (
                    "votonulo",
                    models.IntegerField(default=0, verbose_name="Votos nulos"),
                ),
                (
                    "votoblanco",
                    models.IntegerField(default=0, verbose_name="Votos blanco"),
                ),
                (
                    "cab",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.eventoelectoral",
                        verbose_name="Cab",
                    ),
                ),
            ],
            options={
                "verbose_name": "Detalle Mesa",
                "verbose_name_plural": "Detalles de Mesas",
            },
        ),
        migrations.CreateModel(
            name="SubTablaResultado",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "totalvoto",
                    models.IntegerField(default=0, verbose_name="Total de votos"),
                ),
                (
                    "detallemesa",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.tablaresultado",
                        verbose_name="Detalle de la mesa",
                    ),
                ),
                (
                    "lista",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.listaelectoral",
                        verbose_name="Listas electorales",
                    ),
                ),
            ],
            options={
                "verbose_name": "SubDetalles Mesa",
                "verbose_name_plural": "SubDetalles de Mesas",
            },
        ),
        migrations.AddField(
            model_name="detpersonapadronelectoral",
            name="cab",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="accounts.eventoelectoral",
                verbose_name="Cab",
            ),
        ),
        migrations.AddField(
            model_name="detpersonapadronelectoral",
            name="canton",
            field=models.ForeignKey(
                blank=True,
                max_length=1000,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="accounts.canton",
                verbose_name="Canton",
            ),
        ),
        migrations.AddField(
            model_name="canton",
            name="provincia",
            field=models.ForeignKey(
                blank=True,
                max_length=1000,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="accounts.provincia",
                verbose_name="Provincia",
            ),
        ),
    ]
