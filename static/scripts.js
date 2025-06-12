async function cargarDatos() {
  const res = await fetch('/api/datos');
  const datos = await res.json();

  const contenedor = document.getElementById('datos-container');
  contenedor.innerHTML = '';

  datos.forEach(d => {
    const div = document.createElement('div');
    div.innerHTML = `
      <strong>${d.dispositivo}</strong> - 
      ${d.temperatura}°C, ${d.humedad}% 
      <em>(${new Date(d.timestamp).toLocaleString()})</em>
    `;
    contenedor.appendChild(div);
  });
}

cargarDatos();
setInterval(cargarDatos, 5000); // actualiza cada 5 segundos