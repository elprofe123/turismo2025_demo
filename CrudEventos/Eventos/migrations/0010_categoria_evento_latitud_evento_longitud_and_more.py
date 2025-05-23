# Generated by Django 5.2 on 2025-05-08 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Eventos", "0009_rename_picture_perfil_imagen"),
    ]

    operations = [
        migrations.CreateModel(
            name="Categoria",
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
                ("nombre", models.CharField(max_length=50)),
                ("descripcion", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name="evento",
            name="latitud",
            field=models.DecimalField(
                blank=True, decimal_places=6, max_digits=9, null=True
            ),
        ),
        migrations.AddField(
            model_name="evento",
            name="longitud",
            field=models.DecimalField(
                blank=True, decimal_places=6, max_digits=9, null=True
            ),
        ),
        migrations.AddField(
            model_name="evento",
            name="ubicacion",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="evento",
            name="categorias",
            field=models.ManyToManyField(blank=True, to="Eventos.categoria"),
        ),
    ]
