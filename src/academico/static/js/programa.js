
function cambiar_periodo() {
    var periodo = document.getElementById('periodo').value;
    var url = '/academico/programa/' + periodo;
    window.location.href = url;
}