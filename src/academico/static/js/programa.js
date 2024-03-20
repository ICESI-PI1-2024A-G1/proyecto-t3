changes = {}

function cambiar_periodo() {
    var periodo = document.getElementById('periodo').value;
    var url = '/academico/programas/' + periodo;
    window.location.href = url;
}

function allowdrop(evt) {
    evt.preventDefault();
}

function dragstart(evt){
    evt.dataTransfer.setData('text', evt.target.id);
}

function drop(evt){
    changes[evt.dataTransfer.getData('text')]=evt.target.id;
    document.getElementById(evt.target.id).appendChild(document.getElementById(evt.dataTransfer.getData('text')));
    console.log(changes);
}

function modo_edicion() {
    var elements = document.getElementsByClassName('semestre_malla');
    for (var i = 0; i < elements.length; i++) {
        elements[i].style.backgroundColor = 'rgba(255, 230, 230, 0.773)';
        elements[i].setAttribute('ondrop', 'drop(event)');
        elements[i].setAttribute('ondragover', 'allowdrop(event)');
    }
    var elements = document.getElementsByClassName('semestre_materia');
    for (var i = 0; i < elements.length; i++) {
        elements[i].setAttribute('draggable', 'true');
        elements[i].setAttribute('ondragstart', 'dragstart(event)');
    }
    document.getElementById('btn-guardar').style.display = 'inline';
    document.getElementById('btn-guardar').disabled = false;
    document.getElementById('btn-guardar').classList.remove('btn--disabled');
    document.getElementById('btn-editar').style.display = 'none'; 
}

function guardar_malla() {
    var elements = document.getElementsByClassName('semestre_malla');
    for (var i = 0; i < elements.length; i++) {
        elements[i].style.backgroundColor = '#ebeaea';
        elements[i].setAttribute('ondrop', '');
        elements[i].setAttribute('ondragover', '');
    }
    var elements = document.getElementsByClassName('semestre_materia');
    for (var i = 0; i < elements.length; i++) {
        elements[i].setAttribute('draggable', 'false');
        elements[i].setAttribute('ondragstart', '');
    }
    document.getElementById('btn-guardar').style.display = 'none';
    document.getElementById('btn-editar').style.display = 'inline'; 
    enviar_malla();
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function enviar_malla() {
    periodo = document.getElementById('periodo').value.split('/')[1];
    codigo = document.getElementById('periodo').value.split('/')[0];

    fetch('/academico/programas/'+codigo+"/"+periodo+"/guardar-malla", {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(changes),
    });
    desactivar_guardar();
}

function desactivar_guardar() {
    document.getElementById('btn-guardar').disabled = true;
    document.getElementById('btn-guardar').classList.add('btn--disabled');
}

function activar_guardar(evt) {
    changes[evt.target.id] = evt.target.value
    document.getElementById('btn-guardar').disabled = false;
    document.getElementById('btn-guardar').classList.remove('btn--disabled');
}