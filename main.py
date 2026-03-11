# Ejecutar la app Flask desde fe/ al correr "python main.py" o "uv run main.py" en la raíz
from fe.main import app

if __name__ == "__main__":
    app.run(debug=True, port=5001)
