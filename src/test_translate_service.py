from translate_service import smart_translate, detect_language, translate

def test_detect():
    print("=== DETECT TESTS ===")
    print("ru →", detect_language("Привет, Какие льготы я могу получить?"))
    print("sah →", detect_language("Ханнык многодетнай льготалар баалларый уонна ону хантан ылабын?"))

def test_translate():
    print("=== TRANSLATE TESTS ===")
    print("sah→ru:", translate("Привет, Какие льготы я могу получить?", "ru"))
    print("ru→sah:", translate("Ханнык многодетнай льготалар баалларый уонна ону хантан ылабын?", "sah"))

def test_smart():
    print("=== SMART TRANSLATE ===")
    print(
        smart_translate("Ханнык многодетнай льготалар баалларый уонна ону хантан ылабын?")
    )
    print(
        smart_translate("Привет, Какие льготы я могу получить?")
    )


if __name__ == "__main__":
    test_detect()
    test_translate()
    test_smart()