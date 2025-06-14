let grafico = null;
let intervalo = null;

async function cargarDatos() {
  const cantidad = parseInt(document.getElementById("cantidad").value);
  if (isNaN(cantidad) || cantidad <= 0) return;

  const spinner = document.getElementById("spinner");
  const contenedor = document.getElementById("datos-container");

  spinner.style.display = "block";
  contenedor.innerHTML = "";

  try {
    const response = await fetch(`/api/datos?cantidad=${cantidad}`);
    const datos = await response.json();

    // Invertir para que los datos más viejos estén primero
    const datosOrdenados = datos.slice().reverse();

    // Generar tabla
    const tabla = document.createElement("table");
    tabla.className = "table table-striped table-bordered table-hover align-middle";

    const thead = document.createElement("thead");
    thead.className = "table-primary";
    thead.innerHTML = `
      <tr>
        <th>ID</th>
        <th>Dispositivo</th>
        <th>Temperatura (°C)</th>
        <th>Humedad (%)</th>
        <th>Fecha y hora</th>
      </tr>
    `;

    const tbody = document.createElement("tbody");
    datosOrdenados.forEach(dato => {
      const fila = document.createElement("tr");
      fila.innerHTML = `
        <td>${dato.id}</td>
        <td>${dato.dispositivo}</td>
        <td>${dato.temperatura != null ? dato.temperatura.toFixed(2) : "N/A"}</td>
        <td>${dato.humedad != null ? dato.humedad.toFixed(2) : "N/A"}</td>
        <td>${new Date(dato.timestamp).toLocaleString()}</td>
      `;
      tbody.appendChild(fila);
    });

    tabla.appendChild(thead);
    tabla.appendChild(tbody);
    contenedor.appendChild(tabla);

    // Actualizar gráfico
    actualizarGrafico(datosOrdenados);

  } catch (error) {
    contenedor.innerHTML = `<div class="alert alert-danger">Error cargando datos: ${error}</div>`;
  } finally {
    spinner.style.display = "none";
  }
}

function actualizarGrafico(datos) {
  const ctx = document.getElementById("grafico").getContext("2d");

  const labels = datos.map(d => new Date(d.timestamp).toLocaleTimeString());
  const temperaturas = datos.map(d => d.temperatura);
  const humedades = datos.map(d => d.humedad);

  if (grafico) {
    grafico.destroy();
  }

  grafico = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Temperatura (°C)',
          data: temperaturas,
          borderColor: 'rgba(255, 99, 132, 1)',
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          tension: 0.3
        },
        {
          label: 'Humedad (%)',
          data: humedades,
          borderColor: 'rgba(54, 162, 235, 1)',
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

// Cargar al iniciar
window.onload = () => {
  cargarDatos();
  // Refrescar cada 10 seg
  if (intervalo) clearInterval(intervalo);
  intervalo = setInterval(cargarDatos, 100000);
};
