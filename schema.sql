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
    especialidad  VARCHAR(255)
);

-- =============================================
-- Tabla: citas
-- =============================================
CREATE TABLE citas (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    usuarioId  INT NOT NULL,
    medicoId   INT NOT NULL,
    fecha       DATE NOT NULL,
    hora        TIME NOT NULL,
    estado      VARCHAR(30) NOT NULL DEFAULT 'pendiente',
    motivo      TEXT,
    diagnostico TEXT,
    receta      TEXT,
    FOREIGN KEY (usuarioId) REFERENCES usuarios(id),
    FOREIGN KEY (medicoId) REFERENCES medicos(id)
);

-- =============================================
-- Tabla: historial
-- =============================================
CREATE TABLE historial (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    usuarioId   INT NOT NULL,
    citaId      INT NOT NULL,
    medicoId    INT NOT NULL,
    FOREIGN KEY (usuarioId) REFERENCES usuarios(id),
    FOREIGN KEY (citaId)    REFERENCES citas(id),
    FOREIGN KEY (medicoId)  REFERENCES medicos(id)
);

CREATE INDEX idx_historial_usuarioId ON historial (usuarioId);
CREATE INDEX idx_historial_citaId    ON historial (citaId);
CREATE INDEX idx_historial_medicoId  ON historial (medicoId);
