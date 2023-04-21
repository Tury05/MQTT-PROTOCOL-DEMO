import paho.mqtt.client as mqtt
import datetime
import time
import random
import sys
import multiprocessing

# Configuración del broker de MQTT
broker_address = "localhost"
broker_port = 1883
broker_username = ""
broker_password = ""

# Configuración del entorno
temperature_sensors = ["st-0001", "st-0002", "st-0003", "st-0004", "st-0005"]
consumption_sensors = ["sp-0001", "sp-0002", "sp-0003", "sp-0004", "sp-0005"]

product_ids = ['p-0001', 'p-0002', 'p-0003', 'p-0004','p-0005']
batch_id = sys.argv[1]
mapping_rows = [("m-0001", batch_id),
                ("m-0002", batch_id),
                ("m-0003", batch_id),
                ("m-0004", batch_id),
                ("m-0005", batch_id),]            

len = random.randint(1, 5)
mapping_rows = random.sample(mapping_rows, len)

machines = [i[0] for i in mapping_rows]
temperature_sensors = [x for x in temperature_sensors if x[-4:] in [y[-4:] for y in machines]]
consumption_sensors = [x for x in consumption_sensors if x[-4:] in [y[-4:] for y in machines]]


# Conexión al broker de MQTT
client = mqtt.Client()
#client.username_pw_set(username=broker_username, password=broker_password)
client.connect(broker_address, broker_port)

def send_data(event):
    # Bucle de publicación de mensajes
    while not event.is_set():

        # Publicación del mensaje MQTT con la información del sensor
        for sensor in temperature_sensors:
            temperatura = random.triangular(20, 50, 18)
            now = str(datetime.datetime.utcnow().isoformat())
            client.publish(sensor, f"{temperatura}/{now}")
            if temperatura > 45:
                client.publish('warning/temperature', f"{temperatura}/{sensor}/{now}",  qos=1)
        
        for sensor in consumption_sensors:
            consumo = random.triangular(10, 35, 10)
            now = str(datetime.datetime.utcnow().isoformat())
            client.publish(sensor,  f"{consumo}/{now}")
            if consumo > 30:
                client.publish('warning/consumption', f"{consumo}/{sensor}/{now}",  qos=1)


        # Espera de 60 segundos antes de publicar el siguiente mensaje
        time.sleep(15)

if __name__=="__main__":
    # Obtención de la hora actual en formato ISO 8601
    now = str(datetime.datetime.utcnow().isoformat())
    product = random.choice(product_ids)
    client.publish('start', f"{batch_id}/{mapping_rows}/{product}/{now}")
    
    # Crear el proceso secundario
    evento = multiprocessing.Event()
    p = multiprocessing.Process(target=send_data, args=(evento,))
    
    # Iniciar el proceso secundario
    p.start()
    
    # Esperar a que el usuario escriba "end" en la línea de comandos
    while True:
        entrada = input("Presiona enter para continuar o escribe 'end' para terminar lote de produccion: ")
        if entrada == "end":
            # Detener el proceso secundario
            evento.set()
            p.join()
            
            time.sleep(2)

            now = str(datetime.datetime.utcnow().isoformat())
            client.publish('end', f"{now}",  qos=1)
            time.sleep(2)
            
            break
        elif entrada != "":
            print(f"Entrada no reconocida: {entrada}")
    
    # Esperar a que el proceso secundario termine