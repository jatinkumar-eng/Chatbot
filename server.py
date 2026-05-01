from fastapi import FastAPI
from pydantic import BaseModel
from bot import compose

app = FastAPI()

# -------- Request Models --------
class ComposeRequest(BaseModel):
    category: dict
    merchant: dict
    trigger: dict
    customer: dict | None = None

@app.get("/")
def home():
    return {"message": "Vera Bot API is running 🚀"}


# -------- Endpoint 1: Health Check --------

@app.get("/v1/healthz")
def health():
    return {"status": "ok"}


# -------- Endpoint 2: Metadata --------
@app.get("/v1/metadata")
def metadata():
    return {
        "name": "Vera Bot",
        "version": "1.0",
        "description": "Merchant AI assistant bot"
    }


# -------- Endpoint 3: Context (optional pass-through) --------
@app.post("/v1/context")
def context(data: dict):
    return {"message": "context received"}


# -------- Endpoint 4: Tick (trigger-based message) --------
@app.post("/v1/tick")
def tick(req: ComposeRequest):
    result = compose(req.category, req.merchant, req.trigger, req.customer)
    return result


# -------- Endpoint 5: Reply (multi-turn support) --------
@app.post("/v1/reply")
def reply(req: ComposeRequest):
    result = compose(req.category, req.merchant, req.trigger, req.customer)
    return result


