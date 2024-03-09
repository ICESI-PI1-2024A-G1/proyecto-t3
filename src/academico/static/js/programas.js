function toggleFiltrado() {
    var ordenarPor = document.getElementById('ordenar_por').value;
    var facultadDiv = document.getElementById('facultadDiv');
    var modalidadDiv = document.getElementById('modalidadDiv');
    var estadoDiv = document.getElementById('estadoDiv');

    // Oculta todas las opciones de filtrado
    facultadDiv.style.display = 'none';
    modalidadDiv.style.display = 'none';
    estadoDiv.style.display = 'none';

    // Muestra las opciones de filtrado según el criterio de ordenamiento seleccionado
    if (ordenarPor === 'facultad') {
        facultadDiv.style.display = 'block';
    } else if (ordenarPor === 'modalidad') {
        modalidadDiv.style.display = 'block';
    } else if (ordenarPor === 'estado_solicitud') {
        estadoDiv.style.display = 'block';
    }
}

