function toggleFiltrado() {
    var ordenarPor = document.getElementById('ordenar_por').value;
    var estadoDiv = document.getElementById('estadoDiv');
    var contratoDiv = document.getElementById('contratoDiv');

    // Oculta todas las opciones de filtrado
    estadoDiv.style.display = 'none';
    contratoDiv.style.display = 'none';

    // Muestra las opciones de filtrado según el criterio de ordenamiento seleccionado
    if (ordenarPor === 'estado') {
        estadoDiv.style.display = 'block';
    } else if (ordenarPor === 'contrato_codigo') {
        contratoDiv.style.display = 'block';
    }
}

