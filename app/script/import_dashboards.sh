#!/bin/bash

# Esperar a que Elasticsearch esté disponible
until curl -s http://elasticsearch:9200 > /dev/null; do
  echo "⏳ Esperando a que Elasticsearch esté disponible..."
  sleep 5
done

# Cargar los datos del CSV en Elasticsearch
echo "📊 Cargando datos del CSV en Elasticsearch..."
python /app/main.py
if [ $? -ne 0 ]; then
  echo "❌ Error al cargar los datos del CSV"
  exit 1
fi

# Esperar a que Kibana esté disponible
until curl -s http://kibana:5601 > /dev/null; do
  echo "⏳ Esperando a que Kibana esté disponible..."
  sleep 5
done

# Importar dashboards
echo "📤 Importando dashboards de Kibana..."
curl -X POST "http://kibana:5601/api/saved_objects/_import" \
  -H "kbn-xsrf: true" \
  --form file=@/app/dashboards/kibana_dashboards.ndjson

echo "✅ Proceso completo: datos cargados y dashboards importados"

# Opcional: esperar indefinidamente para mantener el contenedor activo
# tail -f /dev/null