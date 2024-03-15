
function cambiar_periodo() {
    var periodo = document.getElementById('periodo').value;
    var url = '/academico/programas/' + periodo;
    window.location.href = url;
}