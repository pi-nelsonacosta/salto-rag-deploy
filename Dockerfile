# Usar una imagen base de Python 3.10.15
FROM python:3.10.15-slim

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt .

# Crear y activar un entorno virtual
RUN python -m venv /opt/venv

# Activar el entorno virtual y luego instalar las dependencias
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos al contenedor
COPY src/ .

# Exponer el puerto que usa Flask
EXPOSE 5000

# Establecer la ruta del entorno virtual en el PATH
ENV PATH="/opt/venv/bin:$PATH"

# Configurar la variable de entorno de Flask para producción
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
