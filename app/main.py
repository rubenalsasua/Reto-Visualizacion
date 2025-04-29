import pandas as pd
from elasticsearch import Elasticsearch, helpers
import os

# Leer el CSV
df = pd.read_csv('/data/futbol_estad.csv')

# Conexión a Elasticsearch
es = Elasticsearch("http://elasticsearch:9200")

# Esperar hasta que Elasticsearch esté disponible
for _ in range(10):
    try:
        if es.ping():
            print("Elasticsearch listo")
            break
    except ConnectionError:
        print("Esperando a Elasticsearch...")
    time.sleep(5)
else:
    print("No se pudo conectar a Elasticsearch")
    exit(1)

# Nombre del índice
index_name = "futbol_jugadores"

# Crear índice si no existe
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)

# Preparar documentos
def generator(df):
    for _, row in df.iterrows():
        yield {
            "_index": index_name,
            "_source": row.to_dict()
        }

# Insertar documentos con Bulk API
helpers.bulk(es, generator(df))

print(f"Se insertaron {len(df)} documentos en el índice '{index_name}'")
