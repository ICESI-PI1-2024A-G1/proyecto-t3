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

