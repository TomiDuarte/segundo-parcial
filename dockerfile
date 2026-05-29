# Imagen base liviana de Python
FROM python:3.11-slim

# Variables de entorno para Python en contenedores
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar e instalar dependencias primero (mejor uso de caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app/ ./app/

# Exponer el puerto de la app
EXPOSE 8000

# Comando para arrancar la app
# Render y otros PaaS inyectan la variable PORT
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}