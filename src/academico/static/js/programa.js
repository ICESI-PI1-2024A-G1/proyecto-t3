changes = {};
primera_clase = "";

function cambiar_periodo() {
  var periodo = document.getElementById("periodo").value;
  var url = "/academico/programas/" + periodo;
  window.location.href = url;
}

function allowdrop(evt) {
  evt.preventDefault();
}

function dragstart(evt) {
  evt.dataTransfer.setData("text", evt.target.id);
}

function drop(evt) {
  changes[evt.dataTransfer.getData("text")] = evt.target.id;
  document
    .getElementById(evt.target.id)
    .appendChild(document.getElementById(evt.dataTransfer.getData("text")));
}

function modo_edicion() {
  var elements = document.getElementsByClassName("semestre_malla");
  for (var i = 0; i < elements.length; i++) {
    elements[i].style.backgroundColor = "rgba(255, 230, 230, 0.773)";
    elements[i].setAttribute("ondrop", "drop(event)");
    elements[i].setAttribute("ondragover", "allowdrop(event)");
  }
  var elements = document.getElementsByClassName("semestre_materia");
  for (var i = 0; i < elements.length; i++) {
    elements[i].setAttribute("draggable", "true");
    elements[i].setAttribute("ondragstart", "dragstart(event)");
  }
  document.getElementById("btn-guardar").style.display = "inline";
  document.getElementById("btn-guardar").disabled = false;
  document.getElementById("btn-guardar").classList.remove("btn--disabled");
  document.getElementById("btn-editar").style.display = "none";
}

function guardar_malla() {
  var elements = document.getElementsByClassName("semestre_malla");
  for (var i = 0; i < elements.length; i++) {
    elements[i].style.backgroundColor = "#ebeaea";
    elements[i].setAttribute("ondrop", "");
    elements[i].setAttribute("ondragover", "");
  }
  var elements = document.getElementsByClassName("semestre_materia");
  for (var i = 0; i < elements.length; i++) {
    elements[i].setAttribute("draggable", "false");
    elements[i].setAttribute("ondragstart", "");
  }
  document.getElementById("btn-guardar").style.display = "none";
  document.getElementById("btn-editar").style.display = "inline";
  enviar_malla();
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function enviar_malla() {
  periodo = document.getElementById("periodo").value.split("/")[1];
  codigo = document.getElementById("periodo").value.split("/")[0];

  fetch("/academico/programas/" + codigo + "/" + periodo + "/guardar-malla", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(changes),
  });
  desactivar_guardar();
}

function desactivar_guardar() {
  document.getElementById("btn-guardar").disabled = true;
  document.getElementById("btn-guardar").classList.add("btn--disabled");
}

function activar_guardar(evt) {
  changes[evt.target.id] = evt.target.value;
  document.getElementById("btn-guardar").disabled = false;
  document.getElementById("btn-guardar").classList.remove("btn--disabled");
}

function obtener_primera_clase_periodo() {
  var periodo = document.getElementById("periodo_importar").value;
  fetch("/academico/programas/" + periodo + "/obtener-primera-clase")
    .then((response) => response.json())
    .then((data) => {
      if (data["total_clases"] != 0) {
        primera_clase = data["fecha_inicio"];
        document.getElementById("primera-clase").value = formatDate(
          data["fecha_inicio"]
        );
        document.getElementById("form-options").style.display = "block";
        document.getElementById("form-state").textContent =
          "Se importarán un total de " +
          data["total_clases"] +
          " clases a partir de la fecha seleccionada";
      } else {
        primera_clase = "";
        document.getElementById("form-state").textContent =
          "No hay clases registradas en el periodo seleccionado";
        document.getElementById("form-options").style.display = "none";
      }
      document.getElementById("form-state").style.display = "block";
    });
}

function validate_selected_date() {
  var selected_date = document.getElementById("primera-clase-actual").value;
  var oldDate = new Date(primera_clase);
  var date = new Date(selected_date);

  document.getElementById("error-label").style.display = "block";
  if (date.getUTCDate() < oldDate.getUTCDate()) {
    document.getElementById("error-label").textContent =
      "La fecha seleccionada no puede ser anterior a la fecha antigua";
    document.getElementById("submit-import").disabled = true;
  } else if (date.getUTCDay() != oldDate.getUTCDay()) {
    document.getElementById("error-label").textContent =
      "Debe coincidir el día de la semana";
    document.getElementById("submit-import").disabled = true;
  } else {
    document.getElementById("error-label").textContent =
      "Esta acción sobreescribirá toda la malla actual";
    document.getElementById("submit-import").disabled = false;
  }
}

function formatDate(dateString) {
  const diasSemana = [
    "Domingo",
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
  ];
  const meses = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
  ];

  const fecha = new Date(dateString);
  const dayOfWeek = diasSemana[fecha.getUTCDay()];
  const day = fecha.getUTCDate();
  const month = meses[fecha.getUTCMonth()];
  const year = fecha.getUTCFullYear();

  return `${dayOfWeek}, ${day} de ${month} del ${year}`;
}

function cambiar_checkbox_docente() {
  var checkbox = document.getElementById("incluir-docentes");
  checkbox.checked = !checkbox.checked;
}

function send_import_request() {
  document.getElementById("submit-import").disabled = true;
  periodo = document.getElementById("periodo_actual").value;
  codigo = document.getElementById("codigo_programa").value;

  fetch("/academico/programas/" + codigo + "/" + periodo + "/importar", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      primera_clase_actual: document.getElementById("primera-clase-actual")
        .value,
      primera_clase_importar: primera_clase,
      incluir_docentes: document.getElementById("incluir-docentes").checked,
      periodo_importar: document.getElementById("periodo_importar").value,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data["error"]) {
        document.getElementById("form-state").textContent = data["error"];
        document.getElementById("form-state").style.color = "red";
      } else {
        document.getElementById("form-state").textContent = data["success"];
        document.getElementById("form-state").style.color = "green";
      }
      document.getElementById("form-state").style.display = "block";

      // Esperar 2 segundos y recargar la página
      setTimeout(function () {
        location.reload();
      }, 2000);
      
    });
}

function enviar_para_aprobacion() {
  periodo = document.getElementById("periodo").value.split("/")[1];
  codigo = document.getElementById("periodo").value.split("/")[0];

  comentarios = document.getElementById("pp-comentarios").innerHTML;
  document.getElementById("submit-aprobacion").disabled = true;

  fetch(
    "/academico/programas/" + codigo + "/" + periodo + "/enviar-aprobacion",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        comentarios: comentarios,
      }),
    }
  ).then((response) => {
        if (response.status == 404) {
          document.getElementById("form-state-aprobacion").textContent = "Error al enviar";
          document.getElementById("form-state-aprobacion").style.color = "red";
        }else{
            document.getElementById("form-state-aprobacion").textContent = "Enviado correctamente";
        }
        setTimeout(function () {
          location.reload();
        }, 2000);
  });
  
}
