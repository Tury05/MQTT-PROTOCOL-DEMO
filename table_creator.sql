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