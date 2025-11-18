import os
import json
import asyncio
import asyncpg
from datetime import date
from dotenv import load_dotenv

from translation_service import ensure_russian, answer_back_in_original_lang
from semantic_parser import llm_parse_query

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

YANDEX_MODEL_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"


async def db():
    return await asyncpg.connect(DATABASE_URL)

async def load_region_id(conn, code):
    row = await conn.fetchrow("SELECT id FROM region WHERE code = $1", code)
    return row["id"] if row else None

async def load_categories(conn):
    rows = await conn.fetch("SELECT id, name, title FROM beneficiary_category")
    return {r["id"]: r for r in rows}

async def load_benefits(conn, region_id):
    return await conn.fetch("""
        SELECT 
          b.id,
          b.title,
          b.description,
          b.type,
          b.valid_from,
          b.valid_to,
          b.requirements,
          b."howToGet",
          b.source_url,
          array_agg(DISTINCT bbc."categoryId") AS category_ids
        FROM benefit b
        JOIN benefit_region br ON br."benefitId" = b.id
        LEFT JOIN benefit_beneficiary_category bbc ON bbc."benefitId" = b.id
        WHERE br."regionId" = $1
        GROUP BY b.id
    """, region_id)

def score_benefit(benefit, query):
    score = 0
    text = f"{benefit['title']} {benefit['description']}".lower()

    for c in query["categories"]:
        if c.lower() in text:
            score += 4

    for t in query["types"]:
        if t in benefit["type"]:
            score += 3

    for k in query["keywords"]:
        k = k.lower()
        if len(k) >= 4 and k in text:
            score += 1

    vt = benefit.get("valid_to")
    if vt and hasattr(vt, "date") and vt.date() >= date.today():
        score += 1

    return score

async def smart_benefit_search(user_text: str):
    # 1. Перевод
    norm = ensure_russian(user_text)
    text_ru = norm["text_ru"]
    orig_lang = norm["original_lang"]

    # 2. Семантический анализ
    semantic = llm_parse_query(text_ru)

    conn = await db()

    try:
        region_id = await load_region_id(conn, semantic["region_code"])
        categories = await load_categories(conn)
        benefits = await load_benefits(conn, region_id)

        scored = [(score_benefit(b, semantic), b) for b in benefits]
        scored.sort(key=lambda x: x[0], reverse=True)

        top = [x for x in scored if x[0] > 0][:3]
        if not top:
            top = scored[:3]

        items = []
        for sc, b in top:
            cats = []
            for cid in b["category_ids"] or []:
                if cid in categories:
                    cats.append(categories[cid]["title"])

            items.append({
                "id": b["id"],
                "title": b["title"],
                "categories": cats,
                "type": b["type"],
                "valid_to": str(b["valid_to"]),
                "howToGet": b["howToGet"],
                "requirements": b["requirements"],
                "source_url": b["source_url"],
                "score": sc
            })

        # Формируем простой текст
        lines = ["Я нашёл подходящие льготы:\n"]
        for i, it in enumerate(items, 1):
            lines.append(
                f"{i}) {it['title']}\n"
                f"   Категории: {', '.join(it['categories']) or '—'}\n"
                f"   Тип: {it['type']}\n"
                f"   Действует до: {it['valid_to']}\n"
                f"   Как получить: {it['howToGet']}\n"
            )

        answer_ru = "\n".join(lines)

        translated = answer_back_in_original_lang(answer_ru, orig_lang)

        return {
            "query_ru": text_ru,
            "detected_lang": orig_lang,
            "answer_ru": answer_ru,
            "answer_final": translated["answer_final"],
            "items": items
        }

    finally:
        await conn.close()

if __name__ == "__main__":
    import sys, json

    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    try:
        result = asyncio.run(smart_benefit_search(text))
        print(json.dumps({"ok": True, **result}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))