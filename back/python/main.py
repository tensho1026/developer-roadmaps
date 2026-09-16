from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Python backend playground")


class Echo(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"ok": True, "language": "python", "framework": "fastapi"}


@app.post("/echo")
def echo(body: Echo):
    return {"echo": body.message}
