from fastapi import FastAPI

from be.routers import cita as cita_router
from be.routers import medico as medico_router
from be.routers import usuario as usuario_router

app = FastAPI()

app.include_router(usuario_router.router)
app.include_router(medico_router.router)
app.include_router(cita_router.router)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

    """ _port issues_
        Development (auto-reload)
        python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
    """
