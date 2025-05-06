import pandas as pd
from elasticsearch import Elasticsearch, helpers
import os
import time  # Añadido la importación faltante
import sys
from elasticsearch.exceptions import ConnectionError
import logging

# Configuración del logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Nombre del índice global
index_name = "futbol_jugadores"

# Leer el CSV con validación
def load_csv(file_path):
    try:
        if not os.path.exists(file_path):
            logger.error(f"El archivo {file_path} no existe.")
            sys.exit(1)
            
        df = pd.read_csv(file_path)
        
        if df.empty:
            logger.error("El archivo CSV está vacío.")
            sys.exit(1)
            
        logger.info(f"CSV cargado correctamente. {len(df)} filas encontradas.")
        return df
    except Exception as e:
        logger.error(f"Error al leer el CSV: {str(e)}")
        sys.exit(1)

# Usar variables de entorno para la conexión
def connect_to_elasticsearch(url=None, max_retries=60, initial_retry_interval=1):
    url = url or os.environ.get('ELASTICSEARCH_URL', 'http://elasticsearch:9200')
    user = os.environ.get('ELASTICSEARCH_USER')
    password = os.environ.get('ELASTICSEARCH_PASSWORD')

    logger.info(f"Intentando conectar a Elasticsearch en {url}")

    if user and password:
        es = Elasticsearch(
            url,
            basic_auth=(user, password),
            verify_certs=False,
            ssl_show_warn=False
        )
    else:
        es = Elasticsearch(
            url,
            verify_certs=False,
            ssl_show_warn=False
        )

    retry_interval = initial_retry_interval
    for attempt in range(max_retries):
        try:
            if es.ping():
                logger.info(f"Elasticsearch conectado después de {attempt+1} intentos")
                return es
        except ConnectionError:
            logger.warning(f"Esperando a Elasticsearch... Intento {attempt+1}/{max_retries}")
        except Exception as e:
            logger.error(f"Error al conectar: {str(e)}")

        if attempt < max_retries - 1:
            retry_interval = min(retry_interval * 1.5, 30)
            logger.info(f"Esperando {retry_interval:.1f} segundos antes del próximo intento...")
            time.sleep(retry_interval)

    logger.error("No se pudo conectar a Elasticsearch después de varios intentos")
    sys.exit(1)

# Función para preparar documentos
def generator(df):
    for _, row in df.iterrows():
        # Convertir NaN a None para evitar errores
        doc = {k: (None if pd.isna(v) else v) for k, v in row.items()}
        yield {
            "_index": index_name,
            "_source": doc
        }

# Programa principal
if __name__ == "__main__":
    # Cargar el CSV
    file_path = '/data/futbol_estad.csv'
    df = load_csv(file_path)
    
    # Limpiar datos básicos
    df = df.dropna(how='all')
    
    # Conectar a Elasticsearch
    es = connect_to_elasticsearch()
    
    # Crear índice si no existe
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
        logger.info(f"Índice '{index_name}' creado.")
    
    # Insertar documentos con Bulk API
    try:
        success, failed = helpers.bulk(es, generator(df), stats_only=True)
        if failed:
            logger.warning(f"Advertencia: {failed} documentos fallaron durante la inserción")
        logger.info(f"Se insertaron {success} documentos en el índice '{index_name}'")
    except Exception as e:
        logger.error(f"Error durante la inserción: {str(e)}")
        sys.exit(1)
    
    logger.info("Proceso completado exitosamente.")
