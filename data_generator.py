import psycopg2

# Establecer conexión con la base de datos
conexion = psycopg2.connect(
    host="localhost",
    database="Production Line - Buutech",
    user="postgres",
    password="TuryPostgre00"
)

# Crear un cursor para ejecutar consultas
cursor = conexion.cursor()

# -------------------DATA--------------------------
machine_data = [
    ('m-0001', 'laser cutter', 'Wuhan Golden Laser Co.'),
    ('m-0002', 'laser marker', 'Huagong Tech'),
    ('m-0003', 'welder', 'Nordson Corporation'),
    ('m-0004', 'component placement', 'Panasonic'),
    ('m-0005', 'assembler', 'Del-Tron Precision, Inc.')
]

product_data = [
    ('p-0001', 'resistor', ' Electronic component used to limit the electrical current flowing through a circuit.'),
    ('p-0002', 'capacitor', 'Component that store electrical energy in an electric field.'),
    ('p-0003', 'diode', 'Component that allow electric current to flow in one direction and block it in the other.'),
    ('p-0004', 'transistor', ' Component used to amplify or switch electrical signals.'),
    ('p-0005', 'microcontroller', 'Component that contain a processor and other electronic circuits integrated on a single chip.')
]

sensor_data = [
    ('s-0001', 'NTC', 'temperature', 'm-0001'),
    ('s-0002', 'NTC', 'temperature', 'm-0002'),
    ('s-0003', 'RTD', 'temperature', 'm-0003'),
    ('s-0004', 'NTC', 'temperature', 'm-0004'),
    ('s-0005', 'RTD', 'temperature', 'm-0005'),
    ('s-0006', 'CT', 'power consumption', 'm-0001'),
    ('s-0007', 'CT', 'power consumption', 'm-0002'),
    ('s-0008', 'CT', 'power consumption', 'm-0003'),
    ('s-0009', 'CT', 'power consumption', 'm-0004'),
    ('s-0010', 'CT', 'power consumption', 'm-0005')
]
#---------------------------------------------------
# Definir las consultas SQL
machine_insert = "INSERT INTO machine (id, name, manufacturer) VALUES (%s ,%s, %s)"
product_insert = "INSERT INTO product (id, name, description) VALUES (%s ,%s, %s)"
sensor_insert = "INSERT INTO sensor (id, name, type, machine_id) VALUES (%s ,%s, %s, %s)"

# Ejecutar las consultas SQL con los datos
cursor.executemany(machine_insert, [(d[0], d[1], d[2]) for d in machine_data])
cursor.executemany(product_insert, [(d[0], d[1], d[2]) for d in product_data])
cursor.executemany(sensor_insert, [(d[0], d[1], d[2], d[3]) for d in sensor_data])

# Confirmar los cambios en la base de datos
conexion.commit()

# Cerrar la conexión
cursor.close()
conexion.close()