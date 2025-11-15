from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests

# ======================
#  Конфигурация API ключей
# ======================

API_KEY = os.getenv("YANDEX_API_KEY")
FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

if not API_KEY or not FOLDER_ID:
    print("⚠️ WARNING: YANDEX_API_KEY or YANDEX_FOLDER_ID not found in environment variables")

# ======================
#  FastAPI
# ======================

app = FastAPI()


# ======================
#  Яндекс DETECT LANGUAGE
# ======================

def detect_language(text: str) -> str:
    url = "https://translate.api.cloud.yandex.net/translate/v2/detect"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}",
    }

    body = {
        "folderId": FOLDER_ID,
        "text": text,
        "languageCodeHints": ["ru", "sah"]
    }

    r = requests.post(url, json=body, headers=headers)

    try:
        return r.json().get("languageCode")
    except:
        return "unknown"


# ======================
#  Яндекс TRANSLATE
# ======================

def translate(text: str, target_lang: str) -> str:
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}",
    }

    body = {
        "folderId": FOLDER_ID,
        "texts": [text],
        "targetLanguageCode": target_lang
    }

    r = requests.post(url, json=body, headers=headers)

    try:
        return r.json()["translations"][0]["text"]
    except:
        return "Ошибка перевода"


# ======================
#  Интеллектуальный Smart Translate
# ======================

def smart_translate(text: str):
    detected = detect_language(text)

    if detected == "sah":
        # саха → русский
        translated = translate(text, "ru")
    elif detected == "ru":
        # русский → саха
        translated = translate(text, "sah")
    else:
        # fallback: на русский
        translated = translate(text, "ru")

    return {
        "detected": detected,
        "original": text,
        "translated": translated
    }


# ======================
#  Модели FastAPI
# ======================

class TextRequest(BaseModel):
    text: str


# ======================
#  Маршруты API
# ======================

@app.get("/")
def root():
    return {"status": "ok", "message": "Yakut/Russian Translate API running"}


@app.post("/translate")
def translate_route(body: TextRequest):
    return smart_translate(body.text)