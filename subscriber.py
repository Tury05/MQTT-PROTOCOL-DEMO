import paho.mqtt.client as mqtt
import psycopg2

temperature_sensors = ["s-0001", "s-0002", "s-0003", "s-0004", "s-0005"]
consumption_sensors = ["s-0006", "s-0007", "s-0008", "s-0009", "s-0010"]

batch_id = None

# Función para conectarse a la base de datos y almacenar los datos
def insert_data(topic, value):
    global batch_id

    conn = psycopg2.connect(database="Production Line - Buutech", user="postgres", password="TuryPostgre00", host="localhost", port="5432")
    cur = conn.cursor()

    match topic:
        case 'start':
            values = value.split('/')
            batch_id = values[0]
            mapping_rows = [("m-0001", batch_id),
                            ("m-0002", batch_id),
                            ("m-0003", batch_id),
                            ("m-0004", batch_id),
                            ("m-0005", batch_id),]
            
            cur.execute("INSERT INTO production_batch (id, product_id, start_datetime) VALUES (%s, %s, %s)", 
                        (values[0], values[1], values[2]))
            
            cur.executemany("INSERT INTO mapping (machine_id, batch_id) VALUES (%s, %s)", 
                        mapping_rows)
            
            cur.execute("INSERT INTO production_event (datetime, batch_id, type, description) VALUES (%s, %s, 'INFO', 'started producing')", 
                        (values[2], batch_id))
        
        case 'end':
            cur.execute("UPDATE production_batch SET end_datetime = %s WHERE id = %s", 
                        (value, batch_id))
            
            cur.execute("INSERT INTO production_event (datetime, batch_id, type, description) VALUES (%s, %s, 'INFO', 'ended producing')", 
                        (value, batch_id))
        
        case 'warning/temperature':
            values = value.split('/')
            cur.execute("SELECT id FROM measurement WHERE sensor_id = %s AND datetime = %s AND value = %s", (values[1], values[2], values[0]))
            meas_id = cur.fetchall()[0][0]
            
            cur.execute("INSERT INTO production_event (datetime, batch_id, type, measurement_id, description) VALUES (%s, %s, 'WARN', %s, 'high temperature')", 
                        (values[2], batch_id, meas_id))
        
        case 'warning/consumption':
            values = value.split('/')
            cur.execute("SELECT id FROM measurement WHERE sensor_id = %s AND datetime = %s AND value = %s", (values[1], values[2], values[0]))
            meas_id = cur.fetchall()[0][0]
            
            cur.execute("INSERT INTO production_event (datetime, batch_id, type, measurement_id, description) VALUES (%s, %s, 'WARN', %s, 'high consumption')", 
                        (values[2], batch_id, meas_id))
        
        case other:
            values = value.split('/')
            cur.execute("INSERT INTO measurement (datetime, sensor_id, value) VALUES (%s, %s, %s)", (values[1], topic, values[0]))
    
    
    conn.commit()
    conn.close()

# Función para procesar los mensajes recibidos
def on_message(client, userdata, message):
    topic = message.topic
    value = message.payload.decode("utf-8")
    #print(value)
    insert_data(topic, value)

# Configuración del cliente MQTT y suscripción a los temas
client = mqtt.Client()
client.connect("localhost", 1883, 60)

for sensor in temperature_sensors + consumption_sensors:
    client.subscribe(sensor)
client.subscribe('start')
client.subscribe('end')
client.subscribe('warning/temperature')
client.subscribe('warning/consumption')


# Asignación de la función de procesamiento de mensajes
client.on_message = on_message

# Inicio del loop del cliente MQTT
client.loop_forever()