Be: fastapi
Fe: flask
database: mysql

esta es una aplicacion medica con registro y login, al hacer login un usuario pasa a un dashboard adonde puede hacer
citas con distintos medicos de la red. al generar una cita, el medico puede poner lo que paso y guardarse luego como 
parte del historial del usuario. luego cualquier medico puede ver el historial medico ya en proximas citas. 

structura
    folder be - fastapi
    folder fe - flask

entitites
    usuarios
    medicos
        1. dejamos la especialidad como texto
            pros
            cons
        2. crear la tabla pero no mantenerla (agregar una especialidades, sql)
            pros
            cons
        3. crear la tabla y mantenerla (admin - crud)
            pros
            cons