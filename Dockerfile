# Imagen base de Python
FROM python:3.11-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el requirements.txt primero (para aprovechar el caché de Docker)
COPY backend/requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install bcrypt==4.0.1

# Copiamos el resto del código
COPY backend/ .

# Puerto que expone el contenedor
EXPOSE 8000

# Comando para arrancar la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]