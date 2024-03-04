from django.contrib import admin

from academico.models import *

# Register your models here.
admin.site.site_header = 'Sistema Académico'
admin.site.register(Programa)
admin.site.register(EstadoSolicitud)
admin.site.register(TipoDePrograma)
admin.site.register(TipoDeMateria)
admin.site.register(Curso)
admin.site.register(Materia)
admin.site.register(MallaCurricular)
admin.site.register(Facultad)
admin.site.register(Departamento)
admin.site.register(Modalidad)
admin.site.register(Periodo)
admin.site.register(Espacio)
admin.site.register(Clase)
