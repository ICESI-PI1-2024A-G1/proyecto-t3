from django.contrib import admin

from usuarios.models import *

# Register your models here.
admin.site.register(Persona)
admin.site.register(Docente)
admin.site.register(Director)
admin.site.register(Ciudad)
admin.site.register(Contrato)
admin.site.register(EstadoContrato)
admin.site.register(TipoContrato)
