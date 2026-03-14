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

## Entidades

- Usuarios
- Médicos
- Citas
- Historial

### Especialidades — Opciones de diseño

1. **Dejar la especialidad como texto**
   - Pros:
   - Cons:

2. **Crear la tabla pero no mantenerla** *(agregar especialidades vía SQL)*
   - Pros:
   - Cons:

3. **Crear la tabla y mantenerla** *(admin — CRUD)*
   - Pros:
   - Cons:

4. **this is a new feature**
   - Pros:
   - Cons: