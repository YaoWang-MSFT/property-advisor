from fastapi import FastAPI
from app.routes import http_server

app = FastAPI()

app.include_router(http_server.router, prefix="/api")

@app.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}
