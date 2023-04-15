import paho.mqtt.client as mqtt
import psycopg2

temperature_sensors = ["s-001", "s-002", "s-003", "s-004", "s-005"]
consumption_sensors = ["s-006", "s-007", "s-008", "s-009", "s-010"]

# Función para conectarse a la base de datos y almacenar los datos
def insert_data(topic, value):

    values = value.split('/')

    conn = psycopg2.connect(database="Production Line - Buutech", user="postgres", password="TuryPostgre00", host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute("INSERT INTO measurement (datetime, sensor_id, value) VALUES (%s, %s, %s)", (values[1], topic, values[0]))
    conn.commit()
    conn.close()

# Función para procesar los mensajes recibidos
def on_message(client, userdata, message):
    topic = message.topic
    value = message.payload.decode("utf-8")
    print(value)
    insert_data(topic, value)

# Configuración del cliente MQTT y suscripción a los temas
client = mqtt.Client()
client.connect("localhost", 1883, 60)

for sensor in temperature_sensors + consumption_sensors:
    client.subscribe(sensor)

# Asignación de la función de procesamiento de mensajes
client.on_message = on_message

# Inicio del loop del cliente MQTT
client.loop_forever()