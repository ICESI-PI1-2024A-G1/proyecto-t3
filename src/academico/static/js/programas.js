function toggleFiltrado() {
    var ordenarPor = document.getElementById('ordenar_por').value;
    var facultadDiv = document.getElementById('facultadDiv');
    var estadoDiv = document.getElementById('estadoDiv');

    // Oculta todas las opciones de filtrado
    facultadDiv.style.display = 'none';
    estadoDiv.style.display = 'none';

    // Muestra las opciones de filtrado según el criterio de ordenamiento seleccionado
    if (ordenarPor === 'facultad') {
        facultadDiv.style.display = 'block';
    } else if (ordenarPor === 'estado_solicitud') {
        estadoDiv.style.display = 'block';
    }
}

