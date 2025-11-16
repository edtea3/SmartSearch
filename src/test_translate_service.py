from translate_service import smart_translate, detect_language, translate

def test_detect():
    print("=== DETECT TESTS ===")
    print("ru →", detect_language("Привет, Как дела?"))
    print("sah →", detect_language(" буолла?"))

def test_translate():
    print("=== TRANSLATE TESTS ===")
    print("sah→ru:", translate("Куорсун бэйэ", "ru"))
    print("ru→sah:", translate("Привет! Как дела?", "sah"))

def test_smart():
    print("=== SMART TRANSLATE ===")
    print(
        smart_translate("Куорсун бэйэ")
    )
    print(
        smart_translate("Привет, Как дела?")
    )


if __name__ == "__main__":
    test_detect()
    test_translate()
    test_smart()