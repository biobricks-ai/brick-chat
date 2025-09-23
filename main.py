from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from chainlit.utils import mount_chainlit

app = FastAPI()


@app.get("/health")
async def health_check():
    return jsonable_encoder({"status": "healthy"})


mount_chainlit(app=app, target="src/app.py", path="/")
