# Generated by Django 4.2.11 on 2024-04-28 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuario'),
        ('academico', '0005_grupodeclase_curso_intu_generado_espacioclase_and_more'),
        ('solicitud', '0002_propositoviaje_solicitudviatico'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudClases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.clase')),
            ],
        ),
        migrations.RemoveField(
            model_name='solicitudespacio',
            name='espacio',
        ),
        migrations.RemoveField(
            model_name='solicitudespacio',
            name='fecha_fin',
        ),
        migrations.RemoveField(
            model_name='solicitudespacio',
            name='fecha_inicio',
        ),
        migrations.RemoveField(
            model_name='solicitudviatico',
            name='docente',
        ),
        migrations.AddField(
            model_name='solicitudespacio',
            name='estado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='solicitud.estadosolicitud'),
        ),
        migrations.AddField(
            model_name='solicitudespacio',
            name='responsable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.usuario'),
        ),
        migrations.AddField(
            model_name='solicitudviatico',
            name='clase',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='academico.clase'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='fecha_solicitud',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='solicitudviatico',
            name='fecha_ida',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solicitudviatico',
            name='fecha_vuelta',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solicitudviatico',
            name='propositoViaje',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='solicitud.propositoviaje'),
        ),
        migrations.DeleteModel(
            name='SolicitudContable',
        ),
        migrations.DeleteModel(
            name='TipoContable',
        ),
        migrations.AddField(
            model_name='solicitudclases',
            name='solicitud',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solicitud.solicitudespacio'),
        ),
        migrations.AddField(
            model_name='solicitudespacio',
            name='clases',
            field=models.ManyToManyField(through='solicitud.SolicitudClases', to='academico.clase'),
        ),
    ]
