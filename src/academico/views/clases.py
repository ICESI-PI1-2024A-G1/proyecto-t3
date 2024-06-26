from datetime import datetime, timedelta
from django.utils import timezone

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from academico.models import (Clase, Curso, Docente, Espacio, EspacioClase,
                              Estudiante, GrupoDeClase, Modalidad)
from academico.views.common import verificar_permisos
from ccsa_project import settings
from django.contrib import messages
from solicitud.models import (EstadoSolicitud, SolicitudClases,
                              SolicitudEspacio, SolicitudViatico, Usuario)
from django.db.models import Q



def validar_horario(start_day, end_day, grupo_clases):
    
    start_day = timezone.make_aware(start_day)
    end_day = timezone.make_aware(end_day)
    
    for clase in grupo_clases.clase_set.all():
        if (start_day >= clase.fecha_inicio and start_day < clase.fecha_fin) or \
           (end_day > clase.fecha_inicio and end_day <= clase.fecha_fin) or \
           (start_day <= clase.fecha_inicio and end_day >= clase.fecha_fin):
            return False
    return True



@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u,['lideres']))
def solicitar_salones(request, curso_id):
    """
    Vista que permite solicitar salones para las clases de un curso.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        curso_id (int): Recibe el id del curso.

    Returns:
        HttpResponse: La respuesta HTTP que muestra la página de solicitud de salones.
    """
    curso = get_object_or_404(Curso, nrc=curso_id)
    
    request.user.usuario.init_groups()
    if request.method == "POST":

        responsable = Usuario.objects.get(usuario=request.user)
        estado_en_espera, created = EstadoSolicitud.objects.get_or_create(estado=1)
        clase_ids = request.POST.getlist('clases')
        print(f'clase_ids: {clase_ids}')
        if clase_ids:
            clases = Clase.objects.filter(id__in=clase_ids)
            print(f'clases: {clases}')

            for clase in clases:
                if SolicitudClases.objects.filter(clase=clase).exists():
                    print(f'Ya existe una solicitud para la clase {clase.id}')
                    return redirect('visualizar-curso', curso_id=curso.nrc)

            solicitud = SolicitudEspacio.objects.create(responsable=responsable, estado=estado_en_espera)
            for clase in clases:   
                solicitud_clase = SolicitudClases.objects.create(solicitud=solicitud, clase=clase)
                print(f'Solicitud creada para la clase {clase.id}')

        return redirect('visualizar-curso', curso_id=curso.nrc)
    else:
        return redirect('visualizar-curso', curso_id=curso.nrc)

@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u,['gestores']))
def solicitar_viaticos(request, clase_id):
    """
    Crea una nueva solicitud de un viatico para una clase en el sistema.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        clase_id (int): Recibe el id de la clase.

    Returns:
        HttpResponseRedirect: Una redirección a la página de visualizacion del curso.

    Raises:
        Http404: Si la clase no existe.

    """
    clase= get_object_or_404(Clase, id=clase_id)

    request.user.usuario.init_groups()
    if request.method == "POST":
        tiquetesR = request.POST.get("tiquetes", None)
        alimentacionR = request.POST.get("alimentacion", None)
        hospedajeR = request.POST.get("hospedaje", None)
        print("tiq"+str(tiquetesR)+"ali"+str(alimentacionR)+"hospedaje"+str(hospedajeR))
        tiquetes = False
        alimentacion = False
        hospedaje = False
        if(tiquetesR=="on" and tiquetesR!=None):
            tiquetes=True
        if(hospedajeR=="on" and hospedajeR!=None):
            hospedaje=True
        if(alimentacionR=="on" and alimentacionR!=None):
            alimentacion=True
        desc="requirio "+ clase.docente.nombre + " para la clase: "+ str(clase.id) + " en el curso: "+ str(clase.curso.nrc) +"."

        claseBuscar = SolicitudViatico.objects.filter(clase=clase_id).first()
        if(tiquetes or alimentacion or hospedaje):
            if not claseBuscar:
                SolicitudViatico.objects.create(clase=clase, tiquete=tiquetes, hospedaje=hospedaje, alimentacion=alimentacion, descripcion=desc, fecha_solicitud=datetime.now())
                return redirect("visualizar-curso", curso_id=clase.curso.nrc)
            else:
                claseBuscar.alimentacion= alimentacion
                claseBuscar.hospedaje = hospedaje
                claseBuscar.tiquete = tiquetes
                claseBuscar.save()
                return redirect("visualizar-curso", curso_id=clase.curso.nrc)
        else:
            return redirect("visualizar-curso", curso_id=clase.curso.nrc)

@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u,['gestores']))
def editar_tiquete(request, clase_id):
    """
    Edita el valor del atributo tiquete de un viatico a su opuesto.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        clase_id (int): Recibe el id de la clase.

    Returns:
        HttpResponseRedirect: Una redirección a la página de viaticos (listado de solicitudes de viaticos).

    Raises:
        Http404: Si la clase no existe.
    """
    clase= get_object_or_404(Clase, id=clase_id)
    request.user.usuario.init_groups()
    viatico = SolicitudViatico.objects.filter(clase=clase.id).first()
    viatico.tiquete = not viatico.tiquete
    viatico.save()
    return redirect('/solicitud/viaticos')


@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u,['gestores']))
def editar_hospedaje(request, clase_id):
    """
    Edita el valor del atributo hospedaje de un viatico a su opuesto.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        clase_id (int): Recibe el id de la clase.

    Returns:
        HttpResponseRedirect: Una redirección a la página de viaticos (listado de solicitudes de viaticos).

    Raises:
        Http404: Si la clase no existe.
    """
    clase= get_object_or_404(Clase, id=clase_id)
    request.user.usuario.init_groups()
    viatico = SolicitudViatico.objects.filter(clase=clase.id).first()
    viatico.hospedaje = not viatico.hospedaje
    viatico.save()
    return redirect('/solicitud/viaticos')

@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u,['gestores']))
def editar_alimentacion(request, clase_id):
    """
    Edita el valor del atributo alimentacion de un viatico a su opuesto.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        clase_id (int): Recibe el id de la clase.

    Returns:
        HttpResponseRedirect: Una redirección a la página de viaticos (listado de solicitudes de viaticos).

    Raises:
        Http404: Si la clase no existe.
    """
    clase= get_object_or_404(Clase, id=clase_id)
    request.user.usuario.init_groups()
    viatico = SolicitudViatico.objects.filter(clase=clase.id).first()
    viatico.alimentacion = not viatico.alimentacion
    viatico.save()
    return redirect('/solicitud/viaticos')

@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u,['gestores']))
def eliminar_viatico(request, clase_id):
    """
    Elimina un viatico existente.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        clase_id (int): Recibe el id de la clase.

    Returns:
        HttpResponseRedirect: Una redirección a la página de viaticos (listado de solicitudes de viaticos).

    Raises:
        Http404: Si la clase no existe.
    """
    clase= get_object_or_404(Clase, id=clase_id)
    request.user.usuario.init_groups()
    viatico = SolicitudViatico.objects.filter(clase=clase.id).first()
    viatico.delete()
    return redirect('/solicitud/viaticos')


@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u,['lideres']))
def crear_clase(request, curso_id):
    """
    Crea una nueva clase para un curso en el sistema.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        curso_id (int): Recibe el codigo del curso.

    Returns:
        HttpResponseRedirect: Una redirección a la página de visualizacion clases dentro del curso.

    Raises:
        Http404: Si el curso no existe.

    """

    request.user.usuario.init_groups()
    
    if request.method == "POST":
        start_day = datetime.strptime(request.POST.get("start_day"), "%Y-%m-%dT%H:%M")
        end_day = datetime.strptime(request.POST.get("end_day"), "%Y-%m-%dT%H:%M")

        tipo_espacio = int(request.POST.get("tipo_espacio"))
        espacio = Espacio.objects.get(id=tipo_espacio)
        curso = Curso.objects.get(nrc=curso_id)
        modalidad_clase = int(request.POST.get("modalidad_clase"))
        num_semanas_str = request.POST.get("num_semanas", "1")
        num_semanas = int(num_semanas_str) if num_semanas_str else 1
        docente_cedula = request.POST.get("docente_clase")

        if num_semanas > 16:
            messages.error(request, "No se pueden crear más de 18 clases.")
            return redirect("visualizar-curso", curso_id=curso_id)

        if docente_cedula is not None and docente_cedula != "None":
            docente = Docente.objects.get(cedula=docente_cedula)

            clases_conflictivas = Clase.objects.filter(docente=docente).filter(
                Q(fecha_inicio__lt=start_day, fecha_fin__gt=start_day) |
                Q(fecha_inicio__lt=end_day, fecha_fin__gt=end_day)
            )
            if clases_conflictivas.exists():
                messages.error(request, "El docente seleccionado tiene clases conflictivas.")
                return redirect("visualizar-curso", curso_id=curso_id)
            else:
                docente = None

        if espacio.capacidad < curso.cupo:
            messages.error(request, "El espacio seleccionado no tiene la capacidad suficiente para el curso")
            return redirect("visualizar-curso", curso_id=curso_id)

        if not Curso.objects.filter(nrc=curso_id).exists():
            raise Http404("El curso no existe.")

        if not Espacio.objects.filter(id=tipo_espacio).exists():
            raise Http404("El espacio no existe.")

        if not Modalidad.objects.filter(id=modalidad_clase).exists():
            raise Http404("La modalidad no existe.")

        if docente_cedula is not None and docente_cedula != "None":
            docente = Docente.objects.get(cedula=docente_cedula)
        else:
            docente = None

        grupo_clases = GrupoDeClase.objects.create()

        for _ in range(num_semanas):
            clase = Clase.objects.create(
                fecha_inicio=start_day,
                fecha_fin=end_day,
                espacio_asignado=None,
                curso_id=curso_id,
                espacio_id=tipo_espacio,
                modalidad_id=modalidad_clase,
                docente=docente,
                grupo_clases=grupo_clases,
            )
            start_day += timedelta(days=7)
            end_day += timedelta(days=7)

        return redirect("visualizar-curso", curso_id=curso_id)
    return obtener_clases(request, curso_id)
    
@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u,['gestores','directores']))
def obtener_clases(request, curso_id):
    """
    Obtiene las clases de un curso.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        curso_id (int): El código del curso.

    Returns:
        HttpResponse: La respuesta HTTP que muestra la página de visualización de clases.
    """
    
    espacios = Espacio.objects.all()
    modalidades = Modalidad.objects.all()
    docentes = Docente.objects.all()
    return {
        "espacios": espacios,
        "modalidades": modalidades,
        "docentes": docentes,
        "curso_id": curso_id,
    }

@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u,['lideres']))
def editar_clase(request, clase_id):
    """
    Permite editar los atributos de una clase

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        clase_id (int): El código de la clase a editar.


    Returns:
        HttpResponseRedirect: Una redirección a la página de visualizacion clases dentro del curso.

    Raises:
        Http404: Si la clase no existe.

    """
    
    request.user.usuario.init_groups()
    
    clase = get_object_or_404(Clase, id=clase_id)
    if request.method == "POST":
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        tipo_espacio_id = request.POST.get("tipo_espacio_e")
        modalidad_id = request.POST.get("modalidad_clase_e")
        docente_cedula = request.POST.get("docente_clase_e")
        editar_relacionadas = request.POST.get("editar_relacionadas_e")

        if (
            fecha_inicio == None
            or fecha_fin == None
            or tipo_espacio_id == None
            or modalidad_id == None
        ):
            raise Http404("Todos los campos son requeridos.")

        fecha_inicio = datetime.strptime(request.POST.get("fecha_inicio"), "%Y-%m-%dT%H:%M")
        fecha_fin = datetime.strptime(request.POST.get("fecha_fin"), "%Y-%m-%dT%H:%M")
            
        
        try:
            tipo_espacio = Espacio.objects.get(id=tipo_espacio_id)
        except Espacio.DoesNotExist:
            raise Http404("Tipo de espacio no existe.")

        try:
            modalidad = Modalidad.objects.get(id=modalidad_id)
        except Modalidad.DoesNotExist:
            raise Http404("Modalidad no existe.")

        if docente_cedula is not None and docente_cedula != "None":
            try:
                docente = Docente.objects.get(cedula=docente_cedula)

            except Docente.DoesNotExist:
                raise Http404("Docente no existe.")
        else:
            docente = None
        
        conflict = Clase.objects.filter(grupo_clases=clase.grupo_clases).exclude(id=clase_id).filter(
            fecha_inicio__lt=fecha_fin, fecha_fin__gt=fecha_inicio).exists()
        if not conflict:
            
            old_fecha_inicio = clase.fecha_inicio
            old_fecha_fin = clase.fecha_fin
            old_espacio = clase.espacio
            old_modalidad = clase.modalidad
            old_docente = clase.docente

            clase.fecha_inicio = fecha_inicio
            clase.fecha_fin = fecha_fin
            clase.espacio = tipo_espacio
            clase.modalidad = modalidad
            clase.docente = docente
            clase.save()

        if editar_relacionadas:
            for clase_i in Clase.objects.filter(grupo_clases=clase.grupo_clases):
                clase.fecha_inicio
                if clase_i.fecha_inicio > old_fecha_inicio:
                    fecha_inicio += timedelta(days=7)
                    fecha_fin += timedelta(days=7)
                    clase_i.fecha_inicio = fecha_inicio
                    clase_i.fecha_fin = fecha_fin
                    if old_espacio != clase.espacio:
                        clase_i.espacio = tipo_espacio
                    if old_modalidad != clase.modalidad:
                        clase_i.modalidad = modalidad
                    if old_docente != clase.docente:
                        clase_i.docente = docente
                    clase_i.save()

        # Estudiantes
        estudiantes = Estudiante.objects.filter(cursos=clase.curso)
        to_email = []  # List of recipients
        for es in estudiantes:
            to_email.append(es.email)
        # Extracting just the date part from the datetime objects
        fecha_inicio_str = clase.fecha_inicio.date()

        # Extracting just the time part from the datetime objects
        hora_inicio_str = clase.fecha_inicio.time()
        hora_fin_str = clase.fecha_fin.time()

        subject = f"{clase.id} class change"

        if clase.docente is not None:
            nombre_docente = clase.docente.nombre
            to_email.append(clase.docente.email)  # List of recipients
        else:
            nombre_docente = "N/A"

        # Rendering the message using an HTML template
        html_message = render_to_string(
            "email_template.html",
            {
                "fecha_inicio": fecha_inicio_str,
                "tipo_espacio": clase.espacio.tipo,
                "espacio_asignado": clase.espacio_asignado,
                "metodologia": clase.modalidad.metodologia,
                "nombre_docente": nombre_docente,
                "hora_inicio": hora_inicio_str,
                "hora_fin": hora_fin_str,
            },
        )

        from_email = settings.EMAIL_HOST_USER

        # Sending the email with both plain text and HTML content
        if to_email is not None:
            send_mail(
                subject, html_message, from_email, to_email, html_message=html_message
            )

    return redirect("visualizar-curso", curso_id=clase.curso.nrc)


# Create your views here.


@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u,['lideres']))
@require_POST
def eliminar_clase(request, clase_id):
    """
    Elimina una clase del sistema.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        clase_id (int): El ID de la clase a eliminar.

    Returns:
        HttpResponseRedirect: Una redirección a la página de visualización del curso al que pertenecía la clase.
    """
    
    request.user.usuario.init_groups()
    
    if request.method == "POST":
        clase = get_object_or_404(Clase, id=clase_id)
        clase.delete()

        return redirect("visualizar-curso", curso_id=clase.curso.nrc)


@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u,['lideres']))
def nuevas_clases(request,grupo,cantidad):
    """
    Crea nuevas clases para un grupo de clases

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        grupo (int): El ID del grupo de clases al que pertenecen las clases a crear.
        cantidad (int): La cantidad de clases a crear.

    Returns:
        HttpResponseRedirect: Una redirección a la página de visualización del curso al que pertenecía la clase.
    """
    
    request.user.usuario.init_groups()
    
    grupo = get_object_or_404(GrupoDeClase, id=grupo)
    ultima_clase = Clase.objects.filter(grupo_clases=grupo).order_by("fecha_inicio").last()
    curso = Curso.objects.filter(clase=ultima_clase).first()
    
    for i in range(cantidad):
        nueva_clase = Clase.objects.create(
            fecha_inicio=ultima_clase.fecha_inicio + timedelta(days=7),
            fecha_fin=ultima_clase.fecha_fin + timedelta(days=7),
            espacio_asignado=ultima_clase.espacio_asignado,
            curso=ultima_clase.curso,
            espacio=ultima_clase.espacio,
            modalidad=ultima_clase.modalidad,
            docente=ultima_clase.docente,
            grupo_clases=grupo,
        )
        ultima_clase = nueva_clase
    
    
    
    return redirect("visualizar-curso", curso_id=curso.nrc)

@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u,['lideres']))
def eliminar_grupo_de_clases(request, grupo):
    """
    Elimina un grupo de clases del sistema.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        grupo (int): El ID del grupo de clases a eliminar.

    Returns:
        HttpResponseRedirect: Una redirección a la página de visualización del curso al que pertenecía la clase.
    """
    
    request.user.usuario.init_groups()
    
    if request.method == "POST":
        grupo = get_object_or_404(GrupoDeClase, id=grupo)
        curso = Curso.objects.filter(clase__grupo_clases=grupo).first()
        clases = Clase.objects.filter(grupo_clases=grupo)
        clases.delete()
        grupo.delete()
        return redirect("visualizar-curso", curso_id=curso.nrc)
    else:
        return redirect("programas")
