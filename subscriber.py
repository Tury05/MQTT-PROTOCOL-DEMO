import paho.mqtt.client as mqtt
import psycopg2
import random

temperature_sensors = ["st-0001", "st-0002", "st-0003", "st-0004", "st-0005"]
consumption_sensors = ["sp-0001", "sp-0002", "sp-0003", "sp-0004", "sp-0005"]
machines = [("m-0001",), ("m-0002",), ("m-0003",), ("m-0004",), ("m-0005",)]

batch_id = None


# Función para conectarse a la base de datos y almacenar los datos
def insert_data(topic, value):
    global batch_id
    global machines

    conn = psycopg2.connect(database="buutech", user="postgres", password="TuryPostgre00", host="localhost", port="5432")
    cur = conn.cursor()

    match topic:
        case 'start':
            values = value.split('/')
            batch_id = values[0]

            cur.execute("INSERT INTO production_batch (id, product_id, start_datetime) VALUES (%s, %s, %s)", 
                        (values[0], values[2], values[3]))
            
            cur.executemany("INSERT INTO mapping (machine_id, batch_id) VALUES (%s, %s)", 
                        eval(values[1]))
            
            cur.executemany("UPDATE machine SET status = 'Operating' WHERE id = %s", 
                         [(i[0],) for i in eval(values[1])])

            cur.execute("INSERT INTO production_event (datetime, batch_id, type, description) VALUES (%s, %s, 'INFO', 'started producing')", 
                        (values[3], batch_id))
        
        case 'end':
            cur.execute("UPDATE production_batch SET end_datetime = %s WHERE id = %s", 
                        (value, batch_id))
            
            cur.executemany("UPDATE machine SET status = 'Not Operating' WHERE id = %s", 
                        machines)
            
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
def on_message(_client, _userdata, message):
    topic = message.topic
    value = message.payload.decode("utf-8")
    insert_data(topic, value)
if __name__ == '__main__':
    # Configuración del cliente MQTT y suscripción a los temas
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    for sensor in temperature_sensors + consumption_sensors:
        client.subscribe(sensor, qos=1)
    client.subscribe('start', qos=1)
    client.subscribe('end', qos=1)
    client.subscribe('warning/temperature', qos=1)
    client.subscribe('warning/consumption', qos=1)


    # Asignación de la función de procesamiento de mensajes
    client.on_message = on_message

    # Inicio del loop del cliente MQTT
    client.loop_forever()