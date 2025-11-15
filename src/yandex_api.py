import os
import requests

API_KEY = os.getenv("YANDEX_API_KEY")
FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

def detect_language(text: str) -> str:
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

    r = requests.post(url, json=body, headers=headers)
    return r.json().get("languageCode")


def translate_text(text: str, target_lang: str) -> str:
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

    r = requests.post(url, json=body, headers=headers)
    return r.json()["translations"][0]["text"]