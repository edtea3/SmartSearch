import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YANDEX_API_KEY")
FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

if not API_KEY or not FOLDER_ID:
    raise RuntimeError("YANDEX_API_KEY or YANDEX_FOLDER_ID is missing!")


def detect_language(text: str) -> str:
    """Определение языка через Yandex Translate."""
    url = "https://translate.api.cloud.yandex.net/translate/v2/detect"

    body = {
        "folderId": FOLDER_ID,
        "text": text,
        "languageCodeHints": ["ru", "sah"]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}"
    }

    try:
        r = requests.post(url, json=body, headers=headers, timeout=10)
        j = r.json()
        return j.get("languageCode", "unknown")
    except Exception:
        return "unknown"


def translate(text: str, target_lang: str) -> str:
    """Перевод текста через Yandex Translate API."""
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"

    body = {
        "folderId": FOLDER_ID,
        "texts": [text],
        "targetLanguageCode": target_lang
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}"
    }

    try:
        r = requests.post(url, json=body, headers=headers, timeout=10)
        j = r.json()
        return j["translations"][0]["text"]
    except Exception:
        return text


def ensure_russian(text: str):
    """Приводим текст к русскому."""
    lang = detect_language(text)

    if lang == "ru":
        return {"text_ru": text, "original_lang": "ru"}

    text_ru = translate(text, "ru")

    return {
        "text_ru": text_ru,
        "original_lang": lang
    }


def answer_back_in_original_lang(text_ru: str, lang: str):
    """Перевод ответа обратно пользователю."""
    if lang == "ru":
        return {
            "answer_ru": text_ru,
            "answer_final": text_ru
        }

    translated = translate(text_ru, lang)

    return {
        "answer_ru": text_ru,
        "answer_final": translated
    }