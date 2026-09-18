import speech_recognition as sr

IDIOMA = "es-ES"
ESPERA_INICIO = 6
DURACION_MAXIMA = 6
CALIBRACION = 0.4
UMBRAL_PAUSA = 0.8

class ErrorAudio(Exception):
    pass

class servicioAudio:

    def __init__(self):
        self.motor = sr.Recognizer()
        self.motor.pause_threshold = UMBRAL_PAUSA

    def capturarFrase(self):
        try:
            with sr.Microphone() as entrada:
                self.motor.adjust_for_ambient_noise(entrada, duration=CALIBRACION)
                audio = self.motor.listen(
                    entrada, timeout=ESPERA_INICIO, phrase_time_limit=DURACION_MAXIMA
                )
        except OSError as error:
            raise ErrorAudio("No se pudo acceder al micrófono.") from error
        except sr.WaitTimeoutError as error:
            raise ErrorAudio("No se detectó audio, intenta de nuevo.") from error

        try:
            frase = self.motor.recognize_google(audio, language=IDIOMA)
        except sr.UnknownValueError as error:
            raise ErrorAudio("No se entendió lo dictado.") from error
        except sr.RequestError as error:
            raise ErrorAudio("Sin conexión con el servicio de voz.") from error

        return frase.strip()