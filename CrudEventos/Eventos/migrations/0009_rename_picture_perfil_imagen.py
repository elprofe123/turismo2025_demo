# Generated by Django 5.2 on 2025-04-30 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Eventos", "0008_remove_perfil_profile_picture_perfil_picture"),
    ]

    operations = [
        migrations.RenameField(
            model_name="perfil",
            old_name="picture",
            new_name="imagen",
        ),
    ]
