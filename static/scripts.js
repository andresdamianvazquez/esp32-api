async function cargarDatos() {
  const response = await fetch("/api/datos");
  const datos = await response.json();

  const container = document.getElementById("datos-container");

  if (datos.length === 0) {
    container.innerHTML = "<p>No hay datos aún.</p>";
    return;
  }

  // Crear tabla
  let tabla = `
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Dispositivo</th>
          <th>Temperatura (°C)</th>
          <th>Humedad (%)</th>
          <th>Fecha y hora</th>
        </tr>
      </thead>
      <tbody>
  `;

  const etiquetas = [];
  const temperaturas = [];
  const humedades = [];

  datos.reverse().forEach(d => {
    const fecha = new Date(d.timestamp).toLocaleString();
    etiquetas.push(fecha);
    temperaturas.push(d.temperatura);
    humedades.push(d.humedad);

    tabla += `
      <tr>
        <td>${d.id}</td>
        <td>${d.dispositivo}</td>
        <td>${d.temperatura}</td>
        <td>${d.humedad}</td>
        <td>${fecha}</td>
      </tr>
    `;
  });

  tabla += "</tbody></table>";
  container.innerHTML = tabla;

  // Crear gráfico
  const ctx = document.getElementById("grafico").getContext("2d");
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: etiquetas,
      datasets: [
        {
          label: 'Temperatura (°C)',
          data: temperaturas,
          borderColor: 'rgba(255, 99, 132, 1)',
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          fill: false,
          tension: 0.3
        },
        {
          label: 'Humedad (%)',
          data: humedades,
          borderColor: 'rgba(54, 162, 235, 1)',
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          fill: false,
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: 'Últimos datos del ESP32' }
      }
    }
  });
}

window.onload = cargarDatos;
