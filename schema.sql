-- Creación de tablas para med-manage (MariaDB/MySQL)
-- Orden: tablas base primero, luego tablas con FKs

-- =============================================
-- Tabla: usuarios
-- =============================================
CREATE TABLE usuarios (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    name     VARCHAR(255) NOT NULL,
    email    VARCHAR(255) NOT NULL UNIQUE,
    passw    VARCHAR(255) NOT NULL,
    med_info TEXT
);

-- =============================================
-- Tabla: medicos
-- =============================================
CREATE TABLE medicos (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(255) NOT NULL,
    email      VARCHAR(255) NOT NULL UNIQUE,
    specialty  VARCHAR(255)
);

-- =============================================
-- Tabla: citas
-- =============================================
CREATE TABLE citas (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id  INT NOT NULL,
    medico_id   INT NOT NULL,
    fecha       DATE NOT NULL,
    hora        TIME NOT NULL,
    motivo      TEXT,
    diagnostico TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (medico_id) REFERENCES medicos(id)
);

-- =============================================
-- Tabla: historial
-- =============================================
CREATE TABLE historial (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id       INT NOT NULL,
    medico_id        INT NOT NULL,
    fecha            DATE NOT NULL,
    hora             TIME,
    motivo_cita      TEXT,
    diagnosticos     TEXT,
    notas_consultas  TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (medico_id) REFERENCES medicos(id)
);
