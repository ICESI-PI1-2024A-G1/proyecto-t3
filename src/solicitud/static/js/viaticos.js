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
