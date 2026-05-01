from fastapi import FastAPI
from bot import compose

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Vera Bot API is running 🚀"}

@app.get("/v1/healthz")
def health():
    return {"status": "ok"}

@app.get("/v1/metadata")
def metadata():
    return {"name": "Vera Bot", "version": "1.0"}

@app.post("/v1/tick")
def tick(data: dict):
    return compose(
        data.get("category", {}),
        data.get("merchant", {}),
        data.get("trigger", {}),
        data.get("customer")
    )

@app.post("/v1/reply")
def reply(data: dict):
    return compose(
        data.get("category", {}),
        data.get("merchant", {}),
        data.get("trigger", {}),
        data.get("customer")
    )
