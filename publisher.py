import paho.mqtt.client as mqtt
import datetime
import time
import random

# Configuración del broker de MQTT
broker_address = "localhost"
broker_port = 1883
broker_username = ""
broker_password = ""

# Configuración del sensor
temperature_sensors = ["s-0001", "s-0002", "s-0003", "s-0004", "s-0005"]
consumption_sensors = ["s-0006", "s-0007", "s-0008", "s-0009", "s-0010"]

# Conexión al broker de MQTT
client = mqtt.Client()
#client.username_pw_set(username=broker_username, password=broker_password)
client.connect(broker_address, broker_port)

# Bucle de publicación de mensajes
while True:
    # Generación de valores aleatorios de temperatura y consumo
    temperatura = random.uniform(20.0, 25.0)
    consumo = random.uniform(10.0, 15.0)

    # Obtención de la hora actual en formato ISO 8601
    now = datetime.datetime.utcnow().isoformat() + 'Z'

    # Publicación del mensaje MQTT con la información del sensor
    for sensor in temperature_sensors:
        client.publish(sensor, f"{temperatura}/{now}")
    for sensor in consumption_sensors:
        client.publish(sensor,  f"{consumo}/{now}")

    # Espera de 60 segundos antes de publicar el siguiente mensaje
    time.sleep(60)