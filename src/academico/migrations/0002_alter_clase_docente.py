# Generated by Django 5.0.3 on 2024-03-31 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clase',
            name='docente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.docente'),
        ),
    ]
