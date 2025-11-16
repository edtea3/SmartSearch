import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YANDEX_API_KEY")
FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

if not API_KEY or not FOLDER_ID:
    raise RuntimeError("YANDEX_API_KEY or YANDEX_FOLDER_ID environment variable missing!")


def detect_language(text: str) -> str:
    """Определение языка текста через Yandex.Cloud"""
    url = "https://translate.api.cloud.yandex.net/translate/v2/detect"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}"
    }

    body = {
        "folderId": FOLDER_ID,
        "text": text,
        "languageCodeHints": ["ru", "sah"]
    }

    try:
        r = requests.post(url, json=body, headers=headers)
        data = r.json()
        return data.get("languageCode", "unknown")
    except Exception as e:
        print("DETECT ERROR:", e)
        return "unknown"


def translate(text: str, target_lang: str) -> str:
    """Перевод текста на указанный язык"""
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}"
    }

    body = {
        "folderId": FOLDER_ID,
        "texts": [text],
        "targetLanguageCode": target_lang
    }

    try:
        r = requests.post(url, json=body, headers=headers)
        data = r.json()
        return data.get("translations", [{}])[0].get("text", "translation_error")
    except Exception as e:
        print("TRANSLATE ERROR:", e)
        return "translation_error"


def smart_translate(text: str):
    """Умная логика: если текст на саха — переводит на русский,
       если на русском — на саха, иначе на русский."""
    detected = detect_language(text)

    if detected == "sah":
        target = "ru"
    elif detected == "ru":
        target = "sah"
    else:
        target = "ru"  # fallback

    translated = translate(text, target)

    return {
        "detected": detected,
        "target": target,
        "original": text,
        "translated": translated
    }