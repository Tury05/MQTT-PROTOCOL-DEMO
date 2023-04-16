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

# Configuración del sensor
temperature_sensors = ["s-0001", "s-0002", "s-0003", "s-0004", "s-0005"]
consumption_sensors = ["s-0006", "s-0007", "s-0008", "s-0009", "s-0010"]
product_ids = ['p-0001', 'p-0002', 'p-0003', 'p-0004','p-0005']

# Conexión al broker de MQTT
client = mqtt.Client()
#client.username_pw_set(username=broker_username, password=broker_password)
client.connect(broker_address, broker_port)

def send_data():
    # Bucle de publicación de mensajes
    while True:

        # Publicación del mensaje MQTT con la información del sensor
        for sensor in temperature_sensors:
            temperatura = random.uniform(20.0, 50.0)
            now = str(datetime.datetime.utcnow().isoformat())
            client.publish(sensor, f"{temperatura}/{now}")
            if temperatura > 45:
                client.publish('warning/temperature', f"{temperatura}/{sensor}/{now}")
        
        for sensor in consumption_sensors:
            consumo = random.uniform(10.0, 35.0)
            now = str(datetime.datetime.utcnow().isoformat())
            client.publish(sensor,  f"{consumo}/{now}")
            if consumo > 30:
                client.publish('warning/consumption', f"{consumo}/{sensor}/{now}")


        # Espera de 60 segundos antes de publicar el siguiente mensaje
        time.sleep(5)

if __name__=="__main__":
    # Obtención de la hora actual en formato ISO 8601
    now = str(datetime.datetime.utcnow().isoformat())
    product = random.choice(product_ids)
    client.publish('start', f"{sys.argv[1]}/{product}/{now}")
    
    # Crear el proceso secundario
    p = multiprocessing.Process(target=send_data)
    
    # Iniciar el proceso secundario
    p.start()
    
    # Esperar a que el usuario escriba "end" en la línea de comandos
    while True:
        entrada = input("Presiona enter para continuar o escribe 'end' para terminar lote de produccion: ")
        if entrada == "end":
            now = str(datetime.datetime.utcnow().isoformat())
            client.publish('end', f"{now}")
            # Detener el proceso secundario
            p.terminate()
            break
        elif entrada != "":
            print(f"Entrada no reconocida: {entrada}")
    
    # Esperar a que el proceso secundario termine
    p.join()