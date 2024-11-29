// Función para consultar todos los registros
async function consulta_general() {
  try {
    const url = "http://127.0.0.1:5000/";
    const response = await fetch(url);
    const data = await response.json();
    visualizar(data);
  } catch (error) {
    console.error("Error en la consulta general:", error);
  }
}

// Función para visualizar los registros en la tabla
function visualizar(data) {
  let b = "";
  if (data.COFRE) {
    data.COFRE.forEach(item => {
      b += `<tr>
                <td>${item.id_COFRE}</td>
                <td>${item.Plataforma}</td>
                <td>${item.usuario}</td>
                <td>${item.clave}</td>
                <td><button type='button' class="btn btn-info" onclick="location.href='edit.html?variable1=${item.id_COFRE}'">
                  <img src='imagenes/editar.png' height='30' width='30'/>
                </button></td>
                <td><button type='button' class="btn btn-warning" onclick="eliminar(${item.id_COFRE})">
                  <img src='imagenes/delete.png' height='30' width='30'/>
                </button></td>
              </tr>`;
    });
    document.getElementById('data').innerHTML = b;
  }
}

// Función para eliminar un registro
function eliminar(id) {
  let url = "http://127.0.0.1:5000/eliminar/" + id;
  fetch(url, {
    method: 'DELETE'
  })
    .then(response => response.json())
    .then(res => visualizar(res))
    .catch(error => console.error("Error:", error));

  const visualizar = (res) => {
    swal("Mensaje", "Registro eliminado correctamente", "success").then(() => {
      window.location.reload();
    });
  };
}


// Función para registrar un nuevo registro
async function registrar() {
  const url = "http://127.0.0.1:5000/registro/";
  const plat = document.getElementById("Plataforma").value;
  const usua = document.getElementById("usuario").value;
  const clav = document.getElementById("clave").value;

  const data = {
    "Plataforma": plat,
    "usuario": usua,
    "clave": clav
  };

  try {
    const response = await fetch(url, {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    });
    const result = await response.json();
    if (result.mensaje === "Error") {
      swal("Mensaje", "Error en el registro", "error");
    } else {
      swal("Mensaje", "Registro agregado exitosamente", "success");
    }
  } catch (error) {
    console.error("Error en el registro:", error);
    swal("Error", "Hubo un problema al registrar", "error");
  }
}

// Función para consultar un registro individual
async function consulta_individual(id) {
  const url = `http://127.0.0.1:5000/consulta_individual/${id}`;
  try {
    const response = await fetch(url);
    const data = await response.json();
    console.log(data)
    console.log(data.COFRE.id_COFRE)
    //visualizar_individual(data);
    //document.getElementById("id_COFRE").value = data.COFRE.id_COFRE;
    document.getElementById("Plataforma").value = data.COFRE.Plataforma;
    document.getElementById("usuario").value = data.COFRE.usuario;
    document.getElementById("clave").value = data.COFRE.clave;
  } catch (error) {
    console.error("Error al consultar individualmente:", error);
  }
}

// Función para visualizar un solo registro en el formulario de edición
function visualizar_individual(data) {
  //const item = data.COFRE[0]; // Asegurarse de obtener el primer elemento

}

// Función para modificar un registro
async function modificar(id) {
  const url = `http://127.0.0.1:5000/actualizar/${id}`;
  const plat = document.getElementById("Plataforma").value;
  const usua = document.getElementById("usuario").value;
  const clav = document.getElementById("clave").value;

  const data = {
    "Plataforma": plat,
    "usuario": usua,
    "clave": clav
  };

  try {
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      const result = await response.json();
      swal("Mensaje", "Datos actualizados correctamente", "success").then(() => {
        location.href = "index.html"; // O donde quieras redirigir después de la actualización
      });
    } else {
      throw new Error('Error al actualizar los datos');
    }
  } catch (error) {
    console.error("Error al modificar:", error);
    swal("Error", "Hubo un problema al actualizar los datos", "error");
  }
}
