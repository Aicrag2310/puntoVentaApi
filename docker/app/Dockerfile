FROM python:3.8-slim

# Instalar dependencias necesarias para la compilación y otros paquetes
RUN apt update && apt install -y --no-install-recommends gcc default-libmysqlclient-dev curl msodbcsql17

# Copiar los archivos necesarios
WORKDIR /srv/app/
COPY . /srv/app/

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]
