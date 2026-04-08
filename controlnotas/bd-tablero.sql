-- Active: 1772541288694@@127.0.0.1@3306@alumnosadso

CREATE DATABASE IF NOT EXISTS bd_tablero
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE bd_tablero;

CREATE TABLE IF NOT EXISTS usuarios (
    id          INT             NOT NULL AUTO_INCREMENT,
    nombre      VARCHAR(100)    NOT NULL,   -- CORREGIDO: era 'user', debe ser 'nombre'
    password    VARCHAR(255)    NOT NULL,          
    rol         ENUM('admin','docente','viewer') NOT NULL DEFAULT 'viewer',
    creado_en   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_nombre (nombre)           -- CORREGIDO: era uq_user(user)
);


CREATE TABLE IF NOT EXISTS estudiantes (
    id          INT             NOT NULL AUTO_INCREMENT,
    nombre      VARCHAR(150)    NOT NULL,
    edad        TINYINT UNSIGNED NOT NULL,
    carrera     VARCHAR(100)    NOT NULL,
    nota1       DECIMAL(4,2)    NOT NULL DEFAULT 0.00,
    nota2       DECIMAL(4,2)    NOT NULL DEFAULT 0.00,
    nota3       DECIMAL(4,2)    NOT NULL DEFAULT 0.00,
    promedio    DECIMAL(4,2)    GENERATED ALWAYS AS (
                    ROUND((nota1 + nota2 + nota3) / 3, 2)
                ) STORED,
    desempenio  ENUM('Bajo','Medio','Alto') GENERATED ALWAYS AS (
                    CASE
                        WHEN ROUND((nota1 + nota2 + nota3) / 3, 2) < 3.0 THEN 'Bajo'
                        WHEN ROUND((nota1 + nota2 + nota3) / 3, 2) < 4.0 THEN 'Medio'
                        ELSE 'Alto'
                    END
                ) STORED,
    creado_en   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);


INSERT INTO usuarios (nombre, password, rol) VALUES
('admin',    '123', 'admin'),
('profesor', '123', 'docente'),
('invitado', '123', 'viewer');

INSERT INTO estudiantes (nombre, edad, carrera, nota1, nota2, nota3) VALUES
('Paula',  21, 'Fisica',       4.0, 4.5, 3.0),
('Ana',    18, 'Ingenieria',   2.0, 5.0, 3.0),
('Maria',  23, 'Ingenieria',   5.0, 4.5, 3.0),
('Luis',   22, 'Matematicas',  2.0, 3.5, 4.0),
('Maria',  23, 'Ingenieria',   4.0, 3.0, 3.0),
('Carlos', 20, 'Fisica',       3.5, 4.5, 2.0),
('Sofia',      28, 'Fisica',       1.9, 4.1, 2.4),
('Andres',     20, 'Ingenieria',   4.1, 3.9, 4.6),
('Camila',     19, 'Matematicas',  3.6, 1.6, 1.8),
('Juan',       21, 'Quimica',      3.3, 1.6, 2.2),
('Valentina',  28, 'Sistemas',     4.0, 3.0, 3.1),
('Diego',      22, 'Fisica',       4.3, 1.5, 4.3),
('Isabella',   29, 'Ingenieria',   3.0, 2.5, 2.3),
('Miguel',     30, 'Matematicas',  2.7, 1.8, 1.8),
('Daniela',    31, 'Quimica',      2.7, 2.4, 1.7),
('Sebastian',  25, 'Sistemas',     3.4, 4.9, 2.8),
('Laura',      26, 'Fisica',       2.5, 3.7, 4.6),
('Felipe',     23, 'Ingenieria',   3.5, 4.0, 1.7),
('Mariana',    21, 'Matematicas',  4.2, 4.9, 4.5),
('Julian',     31, 'Quimica',      1.9, 2.5, 3.7),
('Natalia',    23, 'Sistemas',     2.1, 2.7, 3.8),
('David',      29, 'Fisica',       4.8, 3.8, 3.6),
('Sara',       20, 'Ingenieria',   3.4, 2.4, 3.1),
('Tomas',      22, 'Matematicas',  5.0, 3.7, 3.4),
('Gabriela',   28, 'Quimica',      2.6, 4.2, 1.7),
('Alejandro',  31, 'Sistemas',     1.6, 2.6, 2.4),
('Melissa',    21, 'Fisica',       4.7, 3.5, 4.0),
('Ricardo',    21, 'Ingenieria',   3.8, 2.9, 4.7),
('Paola',      25, 'Matematicas',  2.0, 2.0, 4.1),
('Esteban',    26, 'Quimica',      2.4, 3.5, 4.6),
('Monica',     24, 'Sistemas',     2.8, 5.0, 2.0);
