import time
from deep_translator import GoogleTranslator, MyMemoryTranslator
from deep_translator.exceptions import TooManyRequests
from langdetect import DetectorFactory, LangDetectException, detect

# Para que langdetect sea determinista
DetectorFactory.seed = 0

# Alias en español/inglés -> código ISO
ALIASES = {
    "ingles": "en", "inglés": "en", "english": "en",
    "espanol": "es", "español": "es", "spanish": "es", "castellano": "es",
    "frances": "fr", "francés": "fr", "french": "fr",
    "aleman": "de", "alemán": "de", "german": "de",
    "italiano": "it", "italian": "it",
    "portugues": "pt", "portugués": "pt", "portuguese": "pt",
    "ruso": "ru", "russian": "ru",
    "japones": "ja", "japonés": "ja", "japanese": "ja",
    "coreano": "ko", "korean": "ko",
    "chino": "zh-CN", "chinese": "zh-CN",
    "arabe": "ar", "árabe": "ar", "arabic": "ar",
    "neerlandes": "nl", "neerlandés": "nl", "dutch": "nl",
    "turco": "tr", "turkish": "tr",
    "polaco": "pl", "polish": "pl", "sueco": "sv", "swedish": "sv",
    "hindi": "hi", "ucraniano": "uk", "rumano": "ro",
}

MYMEMORY_MAP = {
    "en": "en-GB", "es": "es-ES", "fr": "fr-FR", "de": "de-DE",
    "it": "it-IT", "pt": "pt-PT", "ru": "ru-RU", "ja": "ja-JP",
    "ko": "ko-KR", "ar": "ar-SA", "nl": "nl-NL", "zh-CN": "zh-CN",
    "tr": "tr-TR", "pl": "pl-PL", "sv": "sv-SE", "hi": "hi-IN"
}


def _lang(value:str):
    return ALIASES.get(value.strip().lower(), value.strip())


def count_characters(text:str):
    """
    cuenta los caracteres, caracteres sin espacios y palabras de un texto
    Args:
        text: str => el texto a analizar
    """
    try:
        return {
            "caracteres": len(text),
            "caracteres_sin_espacios": len(text.replace(" ", "")),
            "palabras": len(text.split()),
        }
    except Exception as e:
        return str(e)


def detect_language(text:str):
    """
    detecta el idioma en el que esta escrito un texto
    Args:
        text: str => el texto a analizar
    """
    try:
        lang = detect(text)
        return {
            "language_code": lang,
            "language_name": _lang(lang),
        }
    except LangDetectException as e:
        return f"no se pudo detectar el idioma (texto muy corto o ambiguo): {e}"
    except Exception as e:
        return str(e)


def translate_text(text:str, target_lang:str, source_lang:str = "auto"):
    """
    traduce un texto a otro idioma y devuelve la cantidad de caracteres del original
    Args:
        text: str => el texto a traducir
        target_lang: str => el idioma destino
        source_lang: str => el idioma de origen, "auto" para detectar
    """
    try:
        target = _lang(target_lang)
        source = "auto" if source_lang.strip().lower() in ("auto", "automático", "automatico", "") else _lang(source_lang)

        # preservar comillas dobles o simples si el original venia envuelto
        core = text.strip()
        quoted = False
        if len(core) > 2 and ((core.startswith('"') and core.endswith('"')) or (core.startswith("'") and core.endswith("'"))):
            core = core[1:-1].strip()
            quoted = True
        translated=None
        try:
            translated = GoogleTranslator(source=source, target=target).translate(text=core)
        except TooManyRequests:
            # --- INTENTO 2: Fallback a MyMemory ---
            # Nota: MyMemory no usa "auto" en source, si es auto usamos el detectado o "es"
            my_target = MYMEMORY_MAP.get(target,"en-GB") 
            my_source = MYMEMORY_MAP.get(source, "es-ES") if source != "auto" else "es-ES"
            try:
                translated = MyMemoryTranslator(source=my_source, target=my_target).translate(text=core)
            except Exception as e:
                return f"Error de traducción: Google bloqueó la IP y el respaldo falló. Detalle: {e}"

        if not translated:
            return "Error: No se pudo obtener la traducción."

        if quoted:
            translated = f'"{translated}"'

        source_code = source
        if source == "auto":
            try:
                source_code = detect(core)
            except Exception:
                source_code = "auto"


        return {
            "traduccir_texto": translated,
            "lenguaje_origen": source_code,
            "nombre_lenguaje_origen": _lang(source_code),
            "lenguaje_objetivo": target,
            "nombre_lenguaje_objetivo": _lang(target),
            "caracteres": len(text),
            "caracteres_sin_contar_espacio": len(text.replace(" ", "")),
            "palabras": len(text.split()),
        }
    except Exception as e:
        return str(e)