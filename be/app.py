from fastapi import FastAPI

from be.routers import usuario as usuario_router

app = FastAPI()

app.include_router(usuario_router.router)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

    """ _port issues_
        Development (auto-reload)
        python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
    """
