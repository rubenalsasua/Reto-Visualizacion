FROM python:3.12.3

WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY dashboards/kibana_dashboards.ndjson /app/dashboards/
COPY scripts/import_dashboards.sh /app/scripts/

# Dar permisos de ejecución al script
RUN chmod +x /app/scripts/import_dashboards.sh

# Ejecutar el script y luego main.py
CMD ["/bin/bash", "-c", "/app/scripts/import_dashboards.sh && python main.py"]
