## Miembros del equipo
- Manel Díaz
- Rubén Alsasua
- Eneko Saez

## Explicación de los pasos seguidos
1. **Configuración inicial**: Se definieron los contenedores de Elasticsearch, Kibana y la aplicación en `docker-compose.yml`.
2. **Habilitación de seguridad**: Se configuraron contraseñas y tokens para proteger los servicios.
3. **Carga de datos**: Se implementó un script para cargar datos en Elasticsearch y configurar dashboards en Kibana.
4. **Pruebas**: Se verificó la conectividad y funcionalidad de los servicios.

## Instrucciones de uso
1. Clona este repositorio:
   ````
   git clone <url-del-repositorio>
   cd Reto-Visualizacion
   ```
2. Configura las variables de entorno en el archivo `.env`.
3. Inicia los servicios con Docker:
   ```bash
   docker-compose up --build
   ```
4. Accede a los servicios:
   - Elasticsearch: [http://localhost:9200](http://localhost:9200)
   - Kibana: [http://localhost:5601](http://localhost:5601)

## Posibles vías de mejora
- Implementar autenticación basada en OAuth para mayor seguridad.
- Optimizar el rendimiento de los contenedores ajustando los recursos asignados.
- Automatizar la generación de dashboards con scripts más avanzados.

## Problemas / Retos encontrados
- **Conexión inicial**: Dificultades para establecer la conexión entre Kibana y Elasticsearch.
- **Configuración de seguridad**: Ajustar las credenciales y tokens para evitar errores de autenticación.
- **Carga de datos**: Problemas con el formato de los datos al importarlos en Elasticsearch.

## Alternativas posibles
- Usar un servicio gestionado de Elasticsearch y Kibana para evitar configuraciones manuales.
- Reemplazar Docker Compose con Kubernetes para mayor escalabilidad.

