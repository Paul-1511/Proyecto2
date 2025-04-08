Select current_database();

---Se crea la base de datos llamada Reservas 
CREATE DATABASE Reservas;

---Tabla eventos
CREATE TABLE eventos (
id_evento SERIAL PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
fecha TIMESTAMP NOT NULL,
Ubicacion VARCHAR(255) NOT NULL,
descripcion text
);
---Tabla usuarios
CREATE TABLE usuarios (
id_usuario SERIAL PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
email VARCHAR(100) NOT NULL UNIQUE
);
--- Tabla asientos
CREATE TABLE asientos (
id_asiento SERIAL PRIMARY KEY,
id_evento INT NOT NULL,
fila VARCHAR(10) NOT NULL,
numero INT NOT NULL,
tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('VIP', 'General', 'Preferencial')),
    UNIQUE (id_evento, fila, numero),
    FOREIGN KEY (id_evento) REFERENCES eventos(id_evento) ON DELETE CASCADE
);

---Tabla reservas
CREATE TABLE reservas (
id_reserva SERIAL PRIMARY KEY,
id_asiento INT NOT NULL UNIQUE,
id_usuario INT NOT NULL,
fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (id_asiento) REFERENCES asientos(id_asiento) ON DELETE CASCADE,
FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);