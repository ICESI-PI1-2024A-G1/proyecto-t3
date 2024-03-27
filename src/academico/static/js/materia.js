function cambiar_periodo() {
    var periodo = document.getElementById('periodo').value;
    var url = '/academico/materias/' + periodo;
    window.location.href = url;
}
