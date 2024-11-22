FROM python:3.8-slim

WORKDIR /srv/app/
ENV PATH="/srv/app/venv/bin:$PATH"

RUN apt update && apt install -y --no-install-recommends gcc default-libmysqlclient-dev curl

RUN python -m venv venv && \
    pip install -U pip && \
    pip install wheel && \
    pip install "python-dotenv" \
                "fastapi==0.99.*" "ujson==5.7.0" "email-validator==1.3.1" "uvicorn==0.20.0" \
                "python-jose[cryptography]==3.3.*" "passlib[bcrypt]==1.7.*" "python-multipart==0.0.6" \
                "mysqlclient==2.1.1" "SQLAlchemy==1.4.40" "SQLAlchemy-Utils==0.38.2" \
                "python-i18n[YAML]" "openpyxl==3.1.2" "pyodbc==5.1.0" "alembic==1.9.*" \
                "pytz==2024.1" "python-dateutil==2.9.0.post0"

RUN mkdir -p /app/
WORKDIR /app/

# Instalación de Microsoft ODBC driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc > /etc/apt/trusted.gpg.d/microsoft.asc && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17
