import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")
YANDEX_MODEL_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"


def safe_json(text: str):
    try:
        return json.loads(text)
    except:
        return None


def extract_json(text: str):
    if not text:
        return None

    text = text.strip()

    if text.startswith("```"):
        text = text.lstrip("`")
        text = text.rstrip("`")
        text = text.replace("json", "", 1).strip()
        text = text.replace("```", "").strip()

    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == -1:
        return None

    return text[start:end].strip()


def llm_call(prompt: str, max_tokens=600):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YANDEX_API_KEY}"
    }

    body = {
        "modelUri": f"gpt://{YANDEX_FOLDER_ID}/yandexgpt/latest",
        "completionOptions": {"temperature": 0.1, "maxTokens": max_tokens},
        "messages": [{"role": "user", "text": prompt}]
    }

    try:
        response = requests.post(
            YANDEX_MODEL_URL,
            json=body,
            headers=headers,
            timeout=25
        )
        data = response.json()
        return data["result"]["alternatives"][0]["message"]["text"]
    except:
        return ""


def llm_parse_query(text_ru: str):
    prompt = f"""
            Ты — эксперт по льготам России и интеллектуальный парсер.
            Разбери смысл запроса и верни строго JSON.
            
            Запрос: "{text_ru}"
            
            Формат ответа ТОЛЬКО JSON:
            {{
              "categories": [],
              "types": [],
              "region_code": "14",
              "intent": "",
              "keywords": []
            }}
            
            Допустимые categories:
            - PENSIONER
            - LOW_INCOME
            - MULTICHILD_PARENT
            - STUDENT
            - VETERAN
            - DISABLED_1
            - DISABLED_2
            - DISABLED_3
            - DISABLED_CHILD_PARENT
            - RESIDENTS_NORTH_REGIONS
            
            Допустимые types:
            - housing
            - medical
            - transport
            - social
            - federal
            - regional
            - commercial
            - tax
            - family
            - education
            
            Правила:
            - Не придумывай лишнее.
            - Используй только то, что в запросе.
            - region_code по умолчанию: "14".
            - intent — короткая формулировка цели.
            - keywords: 5–10 ключевых слов.
            - НИКАКОГО текста вне JSON.
            """

    raw = llm_call(prompt)
    clean = extract_json(raw)
    j = safe_json(clean)

    if j:
        return j

    return {
        "categories": [],
        "types": [],
        "region_code": "14",
        "intent": "",
        "keywords": text_ru.lower().split()
    }