function changeStateTo(username){
    var form = document.createElement("form");
    form.method = "POST";
    form.action = "/administrador/" + username + "/change_state";
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "csrfmiddlewaretoken";
    input.value = csrfToken;
    form.appendChild(input);
    document.body.appendChild(form);

    form.submit();
}

//To this path: path("administrador/<str:username>/<str:rol>/change_rol", views.change_state, name="change_state")

/**
 * 
 * this view: 
@login_required(login_url="/login")
def change_rol(request, username, rol):
    """
    Vista que permite cambiar el rol de un usuario.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        username (str): El nombre de usuario del usuario a modificar.

    Returns:
        HttpResponse: Una redirección a la página de administrador.
    """
    if username != request.user.username:
        user_to_change = get_object_or_404(User, username=username)
        if rol:
            user_to_change.groups.clear()
            if rol == "Gestor" and user_to_change.rol_principal != "Gestor":
                user_to_change.groups.add(Group.objects.get(name="gestores"))
            
            if rol == "Lider" and user_to_change.rol_principal != "Lider":
                user_to_change.groups.add(Group.objects.get(name="gestores"))
                user_to_change.groups.add(Group.objects.get(name="lideres"))
                
    return redirect("administrador")

 */
function changeRolTo(username, new_rol){
    var form = document.createElement("form");
    form.method = "POST";
    form.action = "/administrador/" + username + "/" + new_rol + "/change_rol";
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "csrfmiddlewaretoken";
    input.value = csrfToken;
    form.appendChild(input);
    document.body.appendChild(form);

    form.submit();

}