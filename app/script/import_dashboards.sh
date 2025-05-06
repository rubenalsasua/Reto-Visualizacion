#!/bin/bash

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

echo "✅ Dashboards importados correctamente"
