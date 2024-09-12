def translate_text(text, to_lang):
    from translate import Translator  # Avoid circular import
    translator = Translator(to_lang=to_lang)
    return translator.translate(text)


translate_text = translate_text("hello", "es")
print(translate_text)