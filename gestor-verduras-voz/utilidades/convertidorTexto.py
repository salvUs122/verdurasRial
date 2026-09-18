import re
import unicodedata

NUMEROS = {
    "cero": 0, "un": 1, "uno": 1, "una": 1, "dos": 2, "tres": 3, "cuatro": 4,
    "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
    "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15,
    "dieciseis": 16, "diecisiete": 17, "dieciocho": 18, "diecinueve": 19,
    "veinte": 20, "veintiuno": 21, "veintidos": 22, "veintitres": 23,
    "veinticuatro": 24, "veinticinco": 25, "treinta": 30, "cuarenta": 40,
    "cincuenta": 50, "sesenta": 60, "setenta": 70, "ochenta": 80, "noventa": 90,
    "cien": 100, "ciento": 100, "doscientos": 200, "trescientos": 300,
    "cuatrocientos": 400, "quinientos": 500,
}
PALABRAS_VACIAS = {"y", "de", "puntos", "bolivianos", "bs"}

def quitarAcentos(texto):
    normalizado = unicodedata.normalize("NFD", texto.lower().strip())
    return "".join(c for c in normalizado if unicodedata.category(c) != "Mn")

def convertirTextoANumero(texto):
    if not texto:
        return None

    limpio = quitarAcentos(texto)

    digitos = re.search(r"\d+", limpio)
    if digitos:
        return int(digitos.group())

    total = 0
    encontrado = False
    for palabra in limpio.split():
        if palabra in PALABRAS_VACIAS:
            continue
        if palabra in NUMEROS:
            total += NUMEROS[palabra]
            encontrado = True
        else:
            return None

    return total if encontrado else None