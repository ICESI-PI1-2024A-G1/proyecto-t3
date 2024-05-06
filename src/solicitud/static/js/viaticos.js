function toggleFiltrado() {
    var ordenarPor = document.getElementById('ordenar_por').value;
    var tiqueteDiv = document.getElementById('tiqueteDiv');
    var hospedajeDiv = document.getElementById('hospedajeDiv');
    var alimentacionDiv = document.getElementById('alimentacionDiv');

    tiqueteDiv.style.display = 'none';
    hospedajeDiv.style.display = 'none';
    alimentacionDiv.style.display = 'none';

    if (ordenarPor === 'tiquete') {
        tiqueteDiv.style.display = 'block';
    } else if (ordenarPor === 'hospedaje') {
        hospedajeDiv.style.display = 'block';
    } else if (ordenarPor === 'alimentacion'){
        alimentacionDiv.style.display = 'block';
    }
}

function confirmarEliminarClase(event, clase_id) {
    var confirmacion = confirm('¿Estás seguro de que quieres eliminar la solicitud de viatico que se hizo a esta clase: '+clase_id+'?');
    if (confirmacion) {
        eliminarViatico(clase_id);
    }
}

function habilitarEdicion(event, idClase) {
    event.preventDefault();
    // Obtén los checkboxes por idClase
    var checkboxTiquete = document.getElementById('tiquete-' + idClase);
    var checkboxHospedaje = document.getElementById('hospedaje-' + idClase);
    var checkboxAlimentacion = document.getElementById('alimentacion-' + idClase);
    // Habilita los checkboxes
    checkboxTiquete.disabled = false;
    checkboxHospedaje.disabled = false;
    checkboxAlimentacion.disabled = false;
}
  

function eliminarViatico(clase_id) {
    var form = document.createElement("form");
    form.method = "POST";
    form.action = "/academico/clases/" + clase_id + "/eliminar_viatico";
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "csrfmiddlewaretoken";
    input.value = csrfToken;
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}

function changeTiquete(clase_id) {
    console.log("aver papito")
    var form = document.createElement("form");
    form.method = "POST";
    form.action = "/academico/clases/" + clase_id + "/editar_tiquete";
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "csrfmiddlewaretoken";
    input.value = csrfToken;
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}

function changeHospedaje(clase_id) {
    var form = document.createElement("form");
    form.method = "POST";
    form.action = "/academico/clases/" + clase_id + "/editar_hospedaje";
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "csrfmiddlewaretoken";
    input.value = csrfToken;
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
    }
function changeAlimentacion(clase_id) {
    var form = document.createElement("form");
    form.method = "POST";
    form.action = "/academico/clases/" + clase_id + "/editar_alimentacion";
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "csrfmiddlewaretoken";
    input.value = csrfToken;
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
    }
