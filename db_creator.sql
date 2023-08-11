CREATE TABLE machine (
   id VARCHAR(50) PRIMARY KEY,
   name VARCHAR (50) NOT NULL,
   manufacturer VARCHAR (50),
   status VARCHAR(50)
);

CREATE TABLE sensor (
   id VARCHAR(50) PRIMARY KEY,
   name VARCHAR(50) NOT NULL,
   type VARCHAR(50) NOT NULL,
   machine_id VARCHAR(50) REFERENCES machine(id)
);

CREATE TABLE measurement (
   id BIGSERIAL PRIMARY KEY,
   datetime timestamp NOT NULL,
   sensor_id VARCHAR(50) NOT NULL REFERENCES sensor(id),
   value FLOAT NOT NULL
);

CREATE TABLE product (
   id VARCHAR(50) PRIMARY KEY,
   name VARCHAR(50) NOT NULL,
   description VARCHAR(255)
);

CREATE TABLE production_batch (
   id VARCHAR(50) PRIMARY KEY,
   product_id VARCHAR(50) NOT NULL REFERENCES product(id),
   start_datetime timestamp NOT NULL,
   end_datetime timestamp
);

CREATE TABLE production_event (
   id BIGSERIAL PRIMARY KEY,
   datetime timestamp NOT NULL,
   batch_id VARCHAR(50) NOT NULL REFERENCES production_batch(id),
   type VARCHAR(50) NOT NULL,
   measurement_id BIGINT REFERENCES measurement(id),
   description VARCHAR(50) NOT NULL
);

CREATE TABLE mapping (
   machine_id VARCHAR(50) REFERENCES machine(id),
   batch_id VARCHAR(50) REFERENCES production_batch(id),
   PRIMARY KEY (machine_id, batch_id)
);

INSERT INTO machine (id, name, manufacturer, status) 
   VALUES ('m-0001', 'laser cutter', 'Wuhan Golden Laser Co.', 'Not Operating');

INSERT INTO machine (id, name, manufacturer, status) 
   VALUES ('m-0002', 'laser marker', 'Huagong Tech', 'Not Operating');

INSERT INTO machine (id, name, manufacturer, status) 
   VALUES ('m-0003', 'welder', 'Nordson Corporation', 'Not Operating');

INSERT INTO machine (id, name, manufacturer, status) 
   VALUES ('m-0004', 'component placement', 'Panasonic', 'Not Operating');

INSERT INTO machine (id, name, manufacturer, status) 
   VALUES ('m-0005', 'assembler', 'Del-Tron Precision, Inc.', 'Not Operating');

INSERT INTO product (id, name, description) 
   VALUES ('p-0001', 'resistor', ' Electronic component used to limit the electrical current flowing through a circuit.');

INSERT INTO product (id, name, description) 
   VALUES ('p-0002', 'capacitor', 'Component that store electrical energy in an electric field.');

INSERT INTO product (id, name, description) 
   VALUES ('p-0003', 'diode', 'Component that allow electric current to flow in one direction and block it in the other.');

INSERT INTO product (id, name, description) 
   VALUES ('p-0004', 'transistor', ' Component used to amplify or switch electrical signals.');

INSERT INTO product (id, name, description) 
   VALUES ('p-0005', 'microcontroller', 'Component that contain a processor and other electronic circuits integrated on a single chip.');

INSERT INTO sensor (id, name, type, machine_id) 
   VALUES ('st-0001', 'NTC', 'temperature', 'm-0001');

INSERT INTO sensor (id, name, type, machine_id) 
   VALUES ('st-0002', 'NTC', 'temperature', 'm-0002');

INSERT INTO sensor (id, name, type, machine_id) 
   VALUES ('st-0003', 'RTD', 'temperature', 'm-0003');

INSERT INTO sensor (id, name, type, machine_id) 
   VALUES ('st-0004', 'NTC', 'temperature', 'm-0004');

INSERT INTO sensor (id, name, type, machine_id) 
   VALUES ('st-0005', 'RTD', 'temperature', 'm-0005');

INSERT INTO sensor (id, name, type, machine_id) 
   VALUES ('sp-0001', 'CT', 'power consumption', 'm-0001');

INSERT INTO sensor (id, name, type, machine_id) 
   VALUES ('sp-0002', 'CT', 'power consumption', 'm-0002');

INSERT INTO sensor (id, name, type, machine_id) 
   VALUES ('sp-0003', 'CT', 'power consumption', 'm-0003');

INSERT INTO sensor (id, name, type, machine_id) 
   VALUES ('sp-0004', 'CT', 'power consumption', 'm-0004');

INSERT INTO sensor (id, name, type, machine_id) 
   VALUES ('sp-0005', 'CT', 'power consumption', 'm-0005');