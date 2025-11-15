import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YANDEX_API_KEY")
FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")


def detect_language(text: str) -> str:
    url = "https://translate.api.cloud.yandex.net/translate/v2/detect"
    headers = {"Content-Type": "application/json", "Authorization": f"Api-Key {API_KEY}"}
    body = {
        "folderId": FOLDER_ID,
        "text": text,
        "languageCodeHints": ["ru", "sah"]
    }

    try:
        r = requests.post(url, json=body, headers=headers)
        return r.json().get("languageCode", "unknown")
    except:
        return "unknown"


def translate(text: str, target_lang: str) -> str:
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"
    headers = {"Content-Type": "application/json", "Authorization": f"Api-Key {API_KEY}"}
    body = {
        "folderId": FOLDER_ID,
        "texts": [text],
        "targetLanguageCode": target_lang
    }

    try:
        r = requests.post(url, json=body, headers=headers)
        data = r.json()
        return data.get("translations", [{}])[0].get("text", "translation_error")
    except:
        return "translation_error"


def smart_translate(text: str):
    detected = detect_language(text)

    if detected == "sah":
        target = "ru"
    elif detected == "ru":
        target = "sah"
    else:
        target = "ru"

    translated = translate(text, target)

    return {
        "detected": detected,
        "target": target,
        "original": text,
        "translated": translated
    }