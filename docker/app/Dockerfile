FROM python:3.8-slim

# Actualiza el sistema e instala las dependencias del sistema necesarias
RUN apt update && apt install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    curl \
    msodbcsql17 \
    libpq-dev  # Si necesitas soporte para PostgreSQL también

# Configura el directorio de trabajo
WORKDIR /srv/app/

# Crear y activar el entorno virtual
RUN python -m venv /srv/app/venv

# Configura el PATH para usar el entorno virtual
ENV PATH="/srv/app/venv/bin:$PATH"

# Actualiza pip y otras herramientas necesarias
RUN pip install --upgrade pip wheel

# Copiar el archivo de requerimientos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Si tienes archivos adicionales que necesitas, cámbialos de lugar aquí
COPY . /srv/app/

# Expón el puerto 8000 para acceder a la app
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]
