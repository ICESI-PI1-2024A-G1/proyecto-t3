from django.contrib import admin

from solicitud.models import *

# Register your models here.
admin.site.register(EstadoSolicitud)
admin.site.register(TipoContable)
admin.site.register(Solicitud)
admin.site.register(SolicitudContable)
admin.site.register(SolicitudEspacio)
admin.site.register(SolicitudViatico)
admin.site.register(PropositoViaje)
