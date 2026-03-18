# py-med-management-app

| Capa       | Tecnología |
|------------|------------|
| Backend    | FastAPI    |
| Frontend   | Flask      |
| Base de datos | MySQL   |

## Descripción

Aplicación médica con registro y login. Al hacer login, un usuario accede a un dashboard donde puede hacer citas con distintos médicos de la red. Al generar una cita, el médico puede registrar lo que ocurrió, guardándose luego como parte del historial del usuario. Cualquier médico puede ver el historial médico en próximas citas.

## Estructura

```
be/   → FastAPI (backend)
fe/   → Flask  (frontend)
```

## Base de datos

> MariaDB / MySQL — ver [`schema.sql`](schema.sql)

### `usuarios`
| Columna  | Tipo         | Notas         |
|----------|--------------|---------------|
| id       | INT (PK)     | auto increment |
| name     | VARCHAR(255) | NOT NULL      |
| email    | VARCHAR(255) | UNIQUE        |
| passw    | VARCHAR(255) | NOT NULL      |
| med_info | TEXT         |               |

### `medicos`
| Columna      | Tipo         | Notas         |
|--------------|--------------|---------------|
| id           | INT (PK)     | auto increment |
| name         | VARCHAR(255) | NOT NULL      |
| email        | VARCHAR(255) | UNIQUE        |
| especialidad | VARCHAR(255) |               |

### `citas`
| Columna     | Tipo     | Notas                    |
|-------------|----------|--------------------------|
| id          | INT (PK) | auto increment            |
| usuarioId   | INT (FK) | → `usuarios(id)`         |
| medicoId    | INT (FK) | → `medicos(id)`          |
| fecha       | DATE     | NOT NULL                 |
| hora        | TIME     | NOT NULL                 |
| estado      | VARCHAR(30) | `pendiente`, `confirmada`, `completada`, `finalizada`, `cancelada` |
| motivo      | TEXT     |                          |
| diagnostico | TEXT     |                          |
| receta      | TEXT     |                          |

Para bases de datos existentes, agrega la nueva columna con:

```sql
ALTER TABLE citas
ADD COLUMN estado VARCHAR(30) NOT NULL DEFAULT 'pendiente';
```

### `historial`
| Columna   | Tipo     | Notas             |
|-----------|----------|-------------------|
| id        | INT (PK) | auto increment     |
| usuarioId | INT (FK) | → `usuarios(id)`  |
| citaId    | INT (FK) | → `citas(id)`     |
| medicoId  | INT (FK) | → `medicos(id)`   |

> Índices de búsqueda en `usuarioId`, `citaId`, `medicoId`.

## Entidades

- Usuarios
- Médicos
- Citas
- Historial

### Especialidades — Opciones de diseño

1. **Dejar la especialidad como texto** *(implementado)*
   - Pros:
   - Cons:

2. **Crear la tabla pero no mantenerla** *(agregar especialidades vía SQL)*
   - Pros:
   - Cons:

3. **Crear la tabla y mantenerla** *(admin — CRUD)*
   - Pros:
   - Cons: