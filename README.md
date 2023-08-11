# Simulador de Envío de Datos de Sensores a Base de Datos a través del Protocolo MQTT

El Simulador de Envío de Datos de Sensores a Base de Datos a través del Protocolo MQTT es una herramienta diseñada para emular y registrar datos de sensores en una base de datos utilizando el protocolo MQTT. Este programa de simulación te permite demostrar y probar el flujo de datos desde sensores ficticios hacia una base de datos, lo cual es especialmente útil para propósitos de desarrollo, pruebas y educación en el campo de la Internet de las cosas (IoT).

## Características Principales

- **Simulación de Sensores:** Crea y simula múltiples sensores virtuales que generan datos de diferentes tipos, como temperatura, humedad, presión, entre otros.

- **Protocolo MQTT:** Utiliza el popular protocolo de mensajería MQTT para enviar y recibir datos simulados de los sensores hacia la base de datos.

- **Base de Datos:** Conecta con una base de datos compatible (por ejemplo, PostgreSQL, MySQL) para almacenar y gestionar los datos de los sensores en tiempo real.

- **Configuración Flexible:** Personaliza fácilmente la frecuencia de generación de datos, los valores límite y los detalles de conexión MQTT y de la base de datos.

## Instalación y Uso

1. Clona este repositorio en tu máquina local.
2. Configura las opciones de simulación en el archivo `config.json`.
3. Instala las dependencias ejecutando `npm install`.
4. Crea la base de datos ejecutando el script `db_creator.sql`.
5. Ejecuta el subscriber ejecutando `python subscriber.py`.
6. Ejecuta el publisher ejecutando `python publisher.py <numero-de-lote>`.

## Consultas

En el archivo `queries.sql` se incluyen algunas consultas de ejemplo.

## Ejemplo de Configuración

```json
{
  "mqtt": {
    "host": "localhost",
    "port": 1883,
    "username": "usuario",
    "password": "contraseña"
  },
  "database": {
    "type": "postgresql",
    "host": "localhost",
    "port": 5432,
    "username": "usuario",
    "password": "contraseña",
    "database": "basededatos"
  }
}```
