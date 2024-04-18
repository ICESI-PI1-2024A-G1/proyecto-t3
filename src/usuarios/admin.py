from django.contrib import admin
from django.contrib.auth.models import Permission

from usuarios.models import *

# Register your models here.
admin.site.register(Persona)
admin.site.register(Docente)
admin.site.register(Director)
admin.site.register(Ciudad)
admin.site.register(Contrato)
admin.site.register(EstadoContrato)
admin.site.register(TipoContrato)
admin.site.register(Permission)
admin.site.register(Usuario)
