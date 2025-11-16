from fastapi import FastAPI
from pydantic import BaseModel
from src.translate_service import smart_translate

app = FastAPI()

class TranslateRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {"status": "ok", "service": "Main backend"}


@app.post("/smart-translate")
def smart_translate_route(body: TranslateRequest):
    return smart_translate(body.text)