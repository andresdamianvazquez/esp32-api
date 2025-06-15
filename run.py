import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render asigna el puerto por variable de entorno
    app.run(host="0.0.0.0", port=port)        # Escuchar en todas las interfaces