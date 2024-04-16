from fastapi import FastAPI

app = FastAPI(
    title="Запись на игру",
    version="0.1",
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


