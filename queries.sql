-- Obtener la cantidad de mediciones realizadas por cada sensor:
SELECT s.id AS sensor_id, s.name AS sensor_name, COUNT(m.id) AS measurement_count
FROM sensor s
LEFT JOIN measurement m ON s.id = m.sensor_id
GROUP BY s.id, s.name;

-- Calcular el promedio de valores medidos por sensor:
SELECT s.id AS sensor_id, s.name AS sensor_name, AVG(m.value) AS average_measurement
FROM sensor s
JOIN measurement m ON s.id = m.sensor_id
GROUP BY s.id, s.name;

-- Encontrar los lotes de producción junto con su cantidad de eventos de producción:
SELECT pb.id AS batch_id, pb.start_datetime, COUNT(pe.id) AS production_event_count
FROM production_batch pb
LEFT JOIN production_event pe ON pb.id = pe.batch_id
GROUP BY pb.id, pb.start_datetime;

-- Calcular la duración promedio de los lotes de producción:
SELECT pb.id AS batch_id, AVG(EXTRACT(EPOCH FROM (pb.end_datetime - pb.start_datetime))) AS avg_production_duration_seconds
FROM production_batch pb
WHERE pb.end_datetime IS NOT NULL;

-- Encontrar los eventos de producción junto con los detalles del producto asociado:
SELECT pe.id AS event_id, pe.datetime, pb.id AS batch_id, p.name AS product_name, p.description AS product_description
FROM production_event pe
JOIN production_batch pb ON pe.batch_id = pb.id
JOIN product p ON pb.product_id = p.id;

-- Encontrar los sensores que tienen mediciones superiores al promedio de valor de todas las mediciones:
SELECT s.id AS sensor_id, s.name AS sensor_name
FROM sensor s
WHERE EXISTS (
    SELECT 1
    FROM measurement m
    WHERE m.sensor_id = s.id
    HAVING AVG(m.value) > (
        SELECT AVG(value) FROM measurement
    )
);

-- Calcular el promedio de mediciones de temperatura por tipo de producto:
SELECT p.name AS product_name, AVG(temperature_count) AS avg_temperature_count
FROM product p
LEFT JOIN (
    SELECT pb.product_id, COUNT(*) AS temperature_count
    FROM production_event pe
    JOIN measurement m ON pe.measurement_id = m.id
    JOIN sensor s ON m.sensor_id = s.id
    JOIN production_batch pb ON pe.batch_id = pb.id
    WHERE s.type = 'temperature'
    GROUP BY pb.product_id
) AS temperatures ON p.id = temperatures.product_id
GROUP BY p.name;

-- Mostrar másquinas con temperaturas superiores a la media:
SELECT m.id AS machine_id, m.name AS machine_name, 
       s.id AS sensor_id, s.name AS sensor_name,
       m_temp.value AS measured_temperature
FROM machine m
JOIN sensor s ON m.id = s.machine_id
JOIN measurement m_temp ON s.id = m_temp.sensor_id
WHERE s.type = 'temperature'
  AND m_temp.value > (
      SELECT AVG(value) FROM measurement WHERE sensor_id = s.id
  );

-- Mostrar másquinas con consumos superiores a la media:
SELECT m.id AS machine_id, m.name AS machine_name, 
       s.id AS sensor_id, s.name AS sensor_name,
       m_power.value AS measured_power_consumption
FROM machine m
JOIN sensor s ON m.id = s.machine_id
JOIN measurement m_power ON s.id = m_power.sensor_id
WHERE s.type = 'power consumption'
  AND m_power.value > (
      SELECT AVG(value) FROM measurement WHERE sensor_id = s.id
  );



