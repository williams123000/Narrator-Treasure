from deep_translator import GoogleTranslator



def translate_text(text):
    # Traduce el texto al español
    translated = GoogleTranslator(source='en', target='es').translate(text)
    return translated
