import json
from src.smart_translate import smart_translate

def handler(request, response):
    try:
        body = request.get_json()
        text = body.get("text", "")
        result = smart_translate(text)

        response.status_code = 200
        return response.send(json.dumps(result), headers={"Content-Type": "application/json"})

    except Exception as e:
        response.status_code = 500
        return response.send(json.dumps({"error": str(e)}))