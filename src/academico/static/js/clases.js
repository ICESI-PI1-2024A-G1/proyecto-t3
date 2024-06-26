function show_pop(clase_id, inicio, fin, espacio, tipo, modalidad, docente, cambiar_otros) {
    clase_seleccionada_id = clase_id;
    console.log(clase_seleccionada_id);
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

    var checkbox = document.getElementById("editar_relacionadas_e");
    if(cambiar_otros==true){
        checkbox.disabled = true;
        document.getElementById("warning-message_e").style.display = "block";
    }else{
        checkbox.disabled = false;
        document.getElementById("warning-message_e").style.display = "none";
    }
    checkbox.checked = cambiar_otros;
}

function show_popViatico(clase_id) {
    popupViaticos.style.display = "block";
    var form = document.getElementById('solicitarViatico');
    form.action = "/academico/clases/" + clase_id + "/solicitar_viatico";

    var tiquetes = document.getElementById("tiquetes");
    console.log(tiquetes,"aaaaaaaaa")
    var hospedaje = document.getElementById("hospedaje");
    var alimentacion = document.getElementById("alimentacion");
    document.getElementById("clase_id").value = clase_id;
    if(tiquetes.checked){
        tiquetes.value="True";
    }
    if(hospedaje.checked){
        hospedaje.value = "True";
    }
    if(alimentacion.checked){
        alimentacion.value = "True";
    }
}

function changeNota(curso,grupoId){
    var form = document.createElement("form");
    form.method = "POST";
    form.action = "/academico/cursos/" + curso + "/" + grupoId +"/change_notas";
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "csrfmiddlewaretoken";
    input.value = csrfToken;
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}

function changeIntu(curso){
    var form = document.createElement("form");
    form.method = "POST";
    form.action = "/academico/cursos/" + curso + "/change_intu";
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "csrfmiddlewaretoken";
    input.value = csrfToken;
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
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

function cambiar_checkbox_edicion(){
    var checkbox = document.getElementById("editar_relacionadas_e");
    if(!checkbox.disabled){
        checkbox.checked = !checkbox.checked;
    }
}

function Solicitud_Salones(){
    var confirmacion = confirm('¿Estás seguro de que quieres solicitar los salones para este curso?');
    if (confirmacion) {
        var checkboxes = document.querySelectorAll('.clase-checkbox');
        var form = document.getElementById("solicitud-form");
        checkboxes.forEach(function(checkbox, index){
            if(checkbox.checked && checkbox.value){
                var input = document.createElement("input");
                input.type = "hidden";
                input.name = "clases";
                input.value = checkbox.value;
                form.appendChild(input);
            }
        });
        form.submit();
    }
}



function display_group(id){
    var group = document.getElementById(id);
    var icon = document.getElementById(id + "_icon");
    if(group.style.display == "none"){
        group.style.display = "flex";
        icon.style.transform = "rotate(-90deg)";
    }else{
        group.style.display = "none";
        icon.style.transform = "rotate(180deg)";
    }
}

var group;
function agregar_en(popup_id, group_id){
    show(popup_id);
    group = group_id;
}

function agregar_clases(){
    numero = document.getElementById("num_semanas_add").value;
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = "/academico/clases/" + group + "/" + numero;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'csrfmiddlewaretoken';
    input.value = csrfToken;
    form.appendChild(input);
    
    document.body.appendChild(form);
    form.submit();
}

function confirmarEliminarGrupo(event, claseId) {
    var confirmacion = confirm('¿Estás seguro de que quieres eliminar este grupo?');
    if (confirmacion) {
        eliminarGrupo(claseId);
    }
}

function eliminarGrupo(grupoId){
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = "/academico/grupo_clases/" + grupoId + "/eliminar";
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'csrfmiddlewaretoken';
    input.value = csrfToken;
    form.appendChild(input);
    
    document.body.appendChild(form);
    form.submit();
}