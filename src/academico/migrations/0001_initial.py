# Generated by Django 5.0.1 on 2024-03-07 14:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('codigo', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Espacio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=10)),
                ('capacidad', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EstadoSolicitud',
            fields=[
                ('estado', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Facultad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Modalidad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('metodologia', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('semestre', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TipoDeMateria',
            fields=[
                ('tipo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='TipoDePrograma',
            fields=[
                ('tipo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('codigo', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('creditos', models.IntegerField()),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('nrc', models.IntegerField(primary_key=True, serialize=False)),
                ('grupo', models.IntegerField()),
                ('cupo', models.IntegerField()),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.materia')),
                ('periodo', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='academico.periodo')),
            ],
        ),
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_inicio', models.DateTimeField(null=True)),
                ('fecha_fin', models.DateTimeField(null=True)),
                ('espacio_asignado', models.CharField(max_length=255, null=True)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.curso')),
                ('espacio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.espacio')),
                ('modalidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.modalidad')),
            ],
        ),
        migrations.CreateModel(
            name='MallaCurricular',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semestre', models.IntegerField()),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.materia')),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.periodo')),
            ],
        ),
        migrations.CreateModel(
            name='Programa',
            fields=[
                ('codigo', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.director')),
                ('estado_solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.estadosolicitud')),
                ('facultad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.facultad')),
                ('tipo_de_programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.tipodeprograma')),
            ],
        ),
        migrations.AddField(
            model_name='materia',
            name='programas',
            field=models.ManyToManyField(through='academico.MallaCurricular', to='academico.programa'),
        ),
        migrations.AddField(
            model_name='mallacurricular',
            name='programa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.programa'),
        ),
        migrations.AddField(
            model_name='materia',
            name='tipo_de_materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.tipodemateria'),
        ),
        migrations.AddConstraint(
            model_name='curso',
            constraint=models.UniqueConstraint(fields=('nrc', 'periodo'), name='unique_nrc_periodo'),
        ),
        migrations.AddConstraint(
            model_name='mallacurricular',
            constraint=models.UniqueConstraint(fields=('materia', 'programa', 'periodo'), name='unique_materia_programa_periodo'),
        ),
    ]
