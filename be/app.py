from fastapi import FastAPI

from be.routers import usuario as usuario_router

app = FastAPI()

app.include_router(usuario_router.router)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
