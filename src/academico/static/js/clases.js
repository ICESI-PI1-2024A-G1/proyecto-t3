function show_pop(evt, inicio, fin, espacio, tipo, modalidad, docente) {
    clase_seleccionada_id = evt.target.id;
    editModal.style.display = "block";
    var form = document.getElementById('editClassForm');
    form.action = "/academico/clases/" + clase_seleccionada_id;

    var fecha_inicio = document.getElementById('fecha_inicio');
    var fecha_fin = document.getElementById('fecha_fin');
    var espacio_asignado = document.getElementById('espacio_asignado');
    var tipo_espacio = document.getElementById('tipo_espacio_e');
    var modalidad_clase = document.getElementById('modalidad_clase_e');
    var docente_clase = document.getElementById('docente_clase_e');

    fecha_inicio.value = format_date(inicio);
    fecha_fin.value = format_date(fin);
    if(espacio == "None"){
        espacio = "Sin asignar";
    }
    espacio_asignado.value = espacio;
    tipo_espacio.value = tipo;
    modalidad_clase.value = modalidad;
    if(docente == ""){
        docente = "None";
    }
    docente_clase.value = docente;
}



function format_date(date){
    var dateF = new Date(convertirFormatoFecha(date));
    var formatted = dateF.getFullYear() + '-' +
                          ('0' + (dateF.getMonth() + 1)).slice(-2) + '-' +
                          ('0' + dateF.getDate()).slice(-2) + 'T' +
                          ('0' + dateF.getHours()).slice(-2) + ':' +
                          ('0' + dateF.getMinutes()).slice(-2);
    return formatted;
}

function convertirFormatoFecha(fechaEnTexto) {
    // Separar la cadena en sus componentes
    var partesFecha = fechaEnTexto.split(/[\s,]+/);

    // Mapear el mes a su número correspondiente
    var meses = {
        "January": "01", "February": "02", "March": "03", "April": "04",
        "May": "05", "June": "06", "July": "07", "August": "08",
        "September": "09", "October": "10", "November": "11", "December": "12"
    };

    // Obtener los componentes de la fecha y hora
    var año = partesFecha[2];
    var mes = meses[partesFecha[0]];
    var dia = ('0' + partesFecha[1]).slice(-2); // Agregar un cero al día si es necesario
    var horaMinuto = partesFecha[3].split(':');
    var hora = ('0' + horaMinuto[0]).slice(-2); // Agregar un cero a la hora si es necesario
    var minutos = ('0' + horaMinuto[1]).slice(-2); // Agregar un cero a los minutos si es necesario
    var ampm = partesFecha[4]; // AM o PM

    // Convertir la hora a formato de 24 horas si es PM
    if (ampm === 'p.m.' && hora !== '12') {
        hora = ('0' + (parseInt(hora) + 12)).slice(-2);
    } else if (ampm === 'a.m.' && hora === '12') {
        hora = '00'; // Convertir 12 AM a 00
    }

    // Construir la cadena en el formato deseado
    var fechaFormateada = año + '-' + mes + '-' + dia + 'T' + hora + ':' + minutos + ':00';

    return fechaFormateada;
}

function confirmarEliminarClase(event, claseId) {
    var confirmacion = confirm('¿Estás seguro de que quieres eliminar esta clase?');
    if (confirmacion) {
        eliminarClase(claseId);
    }
}

function eliminarClase(claseId) {
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = "/academico/clases/" + claseId + "/eliminar";
    
    // Añade el token CSRF a la petición
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'csrfmiddlewaretoken';
    input.value = csrfToken;
    form.appendChild(input);
    
    document.body.appendChild(form);
    form.submit();
}