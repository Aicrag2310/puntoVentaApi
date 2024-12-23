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

# Crea un entorno virtual
RUN python -m venv venv

# Actualiza pip y otras herramientas necesarias
RUN /srv/app/venv/bin/pip install --upgrade pip wheel

# Instala las dependencias de Python desde requirements.txt
COPY requirements.txt .
RUN /srv/app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Si tienes archivos adicionales que necesitas, cámbialos de lugar aquí
COPY . /srv/app/

# Configura el PATH para usar el entorno virtual
ENV PATH="/srv/app/venv/bin:$PATH"

# Instala Microsoft ODBC driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc > /etc/apt/trusted.gpg.d/microsoft.asc && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Expón el puerto 8000 para acceder a la app
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]
