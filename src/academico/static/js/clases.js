function show_pop(evt) {
    clase_seleccionada_id = evt.target.id;
    editModal.style.display = "block";
    var form = document.getElementById('editClassForm');
    form.action = "/academico/clases/" + clase_seleccionada_id;
}
