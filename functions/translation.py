# utils/translation.py
from googletrans import Translator


class Translation:
    @staticmethod
    async def translate_text(text: str, src_lang: str, dest_lang: str) -> str:
        translator = Translator()
        result = await translator.translate(text, src=src_lang, dest=dest_lang)
        return result.text

    @staticmethod
    async def analyze_text(text_complaint: str):
        translator = Translator()

        # 1. Detect language (await required)
        detected = await translator.detect(text_complaint)
        src_lang = detected.lang

        # 2. Translate (await required)
        translated = await translator.translate(text_complaint, src=src_lang, dest="en")
        translated_text = translated.text

        return {
            "detected_language": src_lang,
            "translated_text": translated_text
        }