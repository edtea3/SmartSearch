import json
import requests
import os


API_KEY = os.getenv("YANDEX_API_KEY")
FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")


def detect_language(text: str) -> str:
    url = "https://translate.api.cloud.yandex.net/translate/v2/detect"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}",
    }
    body = {
        "folderId": FOLDER_ID,
        "text": text,
        "languageCodeHints": ["ru", "sah"],
    }

    r = requests.post(url, json=body, headers=headers)
    return r.json().get("languageCode", "ru")


def translate(text: str, target_lang: str) -> str:
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}",
    }
    body = {
        "folderId": FOLDER_ID,
        "texts": [text],
        "targetLanguageCode": target_lang,
    }

    r = requests.post(url, json=body, headers=headers)
    try:
        return r.json()["translations"][0]["text"]
    except:
        return text


def smart_translate(text: str) -> dict:
    lang = detect_language(text)

    if lang == "sah":
        return {
            "detected": "sah",
            "translated": translate(text, "ru"),
            "target_lang": "ru"
        }

    if lang == "ru":
        return {
            "detected": "ru",
            "translated": translate(text, "sah"),
            "target_lang": "sah"
        }

    return {
        "detected": lang,
        "translated": translate(text, "ru"),
        "target_lang": "ru"
    }


def handler(request):
    try:
        body = json.loads(request.body.decode())
        text = body.get("text", "")

        if not text:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "text is required"})
            }

        result = smart_translate(text)

        return {
            "statusCode": 200,
            "body": json.dumps(result, ensure_ascii=False)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }