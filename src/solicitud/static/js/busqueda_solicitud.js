function filtrado_busqueda() {
    var ordenarPor = document.getElementById('ordenar_por').value;
    var estado_salonDiv = document.getElementById('estado_salonDiv');
    var responsableDiv = document.getElementById('responsableDiv');

    // Oculta todas las opciones de filtrado
    estado_salonDiv.style.display = 'none';
    responsableDiv.style.display = 'none';

    // Muestra las opciones de filtrado según el criterio de ordenamiento seleccionado
    if (ordenarPor === 'estado') {
        estado_salonDiv.style.display = 'block';
    } else if (ordenarPor === 'responsable') {
        responsableDiv.style.display = 'block';
    }
}