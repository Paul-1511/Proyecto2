-- Insertar datos en la tabla eventos
INSERT INTO eventos (nombre, fecha, Ubicacion, descripcion) VALUES
('Concierto de Rock', '2023-11-15 20:00:00', 'Estadio Nacional', 'Concierto de las mejores bandas de rock internacional'),
('Obra de Teatro: Hamlet', '2023-12-05 19:30:00', 'Teatro Municipal', 'Clásica obra de Shakespeare con actores reconocidos'),
('Partido de Fútbol: Nacional vs Internacional', '2023-11-20 17:00:00', 'Estadio Centenario', 'Partido amistoso entre equipos locales e internacionales'),
('Festival de Jazz', '2023-12-10 18:00:00', 'Plaza Principal', 'Festival al aire libre con músicos de jazz de todo el mundo'),
('Conferencia de Tecnología', '2023-11-25 09:00:00', 'Centro de Convenciones', 'Evento sobre las últimas tendencias en tecnología e innovación');

-- Insertar datos en la tabla usuarios
INSERT INTO usuarios (nombre, email) VALUES
('Juan Pérez', 'juan.perez@email.com'),
('María García', 'maria.garcia@email.com'),
('Carlos López', 'carlos.lopez@email.com'),
('Ana Martínez', 'ana.martinez@email.com'),
('Luis Rodríguez', 'luis.rodriguez@email.com'),
('Sofía Fernández', 'sofia.fernandez@email.com'),
('Pedro González', 'pedro.gonzalez@email.com'),
('Laura Sánchez', 'laura.sanchez@email.com'),
('Jorge Ramírez', 'jorge.ramirez@email.com'),
('Mónica Díaz', 'monica.diaz@email.com');

-- Insertar datos en la tabla asientos (para el Concierto de Rock)
INSERT INTO asientos (id_evento, fila, numero, tipo) VALUES
(1, 'A', 1, 'VIP'),
(1, 'A', 2, 'VIP'),
(1, 'A', 3, 'VIP'),
(1, 'B', 1, 'Preferencial'),
(1, 'B', 2, 'Preferencial'),
(1, 'B', 3, 'Preferencial'),
(1, 'C', 1, 'General'),
(1, 'C', 2, 'General'),
(1, 'C', 3, 'General'),
(1, 'C', 4, 'General'),
(1, 'C', 5, 'General');

-- Insertar datos en la tabla asientos (para la Obra de Teatro)
INSERT INTO asientos (id_evento, fila, numero, tipo) VALUES
(2, 'A', 1, 'VIP'),
(2, 'A', 2, 'VIP'),
(2, 'A', 3, 'VIP'),
(2, 'B', 1, 'Preferencial'),
(2, 'B', 2, 'Preferencial'),
(2, 'B', 3, 'Preferencial'),
(2, 'C', 1, 'General'),
(2, 'C', 2, 'General'),
(2, 'C', 3, 'General');

-- Insertar datos en la tabla reservas
INSERT INTO reservas (id_asiento, id_usuario, fecha_reserva) VALUES
(1, 1, '2023-10-01 10:00:00'),  -- Juan Pérez reserva asiento VIP A1 para el concierto
(4, 2, '2023-10-02 11:30:00'),  -- María García reserva asiento Preferencial B1 para el concierto
(7, 3, '2023-10-03 09:15:00'),  -- Carlos López reserva asiento General C1 para el concierto
(10, 4, '2023-10-04 14:20:00'), -- Ana Martínez reserva asiento General C4 para el concierto
(12, 5, '2023-10-05 16:45:00'), -- Luis Rodríguez reserva asiento VIP A1 para la obra
(15, 6, '2023-10-06 12:10:00'), -- Sofía Fernández reserva asiento Preferencial B3 para la obra
(18, 7, '2023-10-07 13:30:00'); -- Pedro González reserva asiento General C3 para la obra

-- Actualizar el email de un usuario
UPDATE usuarios SET email = 'juan.perez.nuevo@email.com' WHERE id_usuario = 1;

-- Actualizar la descripción de un evento
UPDATE eventos SET descripcion = 'Concierto de rock con bandas internacionales y artistas invitados' WHERE id_evento = 1;

-- Eliminar una reserva (por ejemplo, si fue cancelada)
DELETE FROM reservas WHERE id_reserva = 7;

-- Consultas de ejemplo para verificar los datos
SELECT * FROM eventos;
SELECT * FROM usuarios;
SELECT * FROM asientos;
SELECT * FROM reservas;