from fastapi import FastAPI
from bot import compose

app = FastAPI()

# -------------------------------
# Root (optional)
# -------------------------------
@app.get("/")
def root():
    return {"message": "Vera Bot API is running 🚀"}


# -------------------------------
# Health check
# -------------------------------
@app.get("/v1/healthz")
def health():
    return {"status": "ok"}


# -------------------------------
# Metadata
# -------------------------------
@app.get("/v1/metadata")
def metadata():
    return {
        "name": "Vera Bot",
        "version": "1.0",
        "description": "Merchant AI assistant bot"
    }


# -------------------------------
# Context endpoint (NEW)
# -------------------------------
@app.post("/v1/context")
def context(data: dict):
    # You can store or process context if needed
    return {
        "status": "context received",
        "received_keys": list(data.keys())
    }


# -------------------------------
# Main tick endpoint
# -------------------------------
@app.post("/v1/tick")
def tick(data: dict):
    return compose(
        data.get("category", {}),
        data.get("merchant", {}),
        data.get("trigger", {}),
        data.get("customer")
    )


# -------------------------------
# Reply endpoint
# -------------------------------
@app.post("/v1/reply")
def reply(data: dict):
    return compose(
        data.get("category", {}),
        data.get("merchant", {}),
        data.get("trigger", {}),
        data.get("customer")
    )
