from src.yandex_api import detect_language, translate_text

def smart_translate(text: str) -> dict:
    lang = detect_language(text)

    if lang == "sah":
        translated = translate_text(text, "ru")
        return {
            "detected": lang,
            "original": text,
            "translated": translated,
            "target_lang": "ru"
        }

    elif lang == "ru":
        translated = translate_text(text, "sah")
        return {
            "detected": lang,
            "original": text,
            "translated": translated,
            "target_lang": "sah"
        }

    else:
        translated = translate_text(text, "ru")
        return {
            "detected": lang,
            "original": text,
            "translated": translated,
            "target_lang": "ru"
        }