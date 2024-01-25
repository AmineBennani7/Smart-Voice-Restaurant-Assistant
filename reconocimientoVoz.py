 ##pip install speech_recognition
import speech_recognition as sr

class ReconocimientoVoz:
    def __init__(self, language='es-ES'):
        self.language = language
        self.recognizer = sr.Recognizer()

    def insert_audio(self):
        with sr.Microphone() as source:
            print("Di algo...")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text
        except sr.UnknownValueError:
            print("No se pudo reconocer el audio.")
            return ""
        except sr.RequestError as e:
            print("Error al realizar la solicitud: {0}".format(e))
            return ""

# Uso de la clase (TEST)
reconocedor = ReconocimientoVoz()
texto_reconocido = reconocedor.insert_audio()
print("Texto reconocido:", texto_reconocido)


