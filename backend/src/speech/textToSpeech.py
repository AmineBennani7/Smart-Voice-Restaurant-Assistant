# pip install gTTS pyttxx playsound
#pip install --upgrade wheel
#pip install pydub
#pip install pygame


#https://thepythoncode.com/article/convert-text-to-speech-in-python

from gtts import gTTS
import pygame
import os

def text_to_speech(text):
    # Directorio del script
    script_dir = os.path.dirname(__file__)

    # Nombre del archivo de salida MP3
    mp3_file = os.path.join(script_dir, "output.mp3")

    # Crear objeto gTTS
    tts = gTTS(text, lang='es-us')

    try:
        # Guardar el archivo MP3
        tts.save(mp3_file)
        print(f"Archivo MP3 guardado en: {mp3_file}")
    except Exception as e:
        print(f"Error al guardar el archivo MP3: {e}")

    return mp3_file

def reproducir_mp3(ruta_archivo):
    # Inicializar pygame
    pygame.init()

    # Inicializar el módulo de audio
    pygame.mixer.init()

    try:
        # Cargar el archivo MP3
        pygame.mixer.music.load(ruta_archivo)

        # Reproducir el archivo MP3
        pygame.mixer.music.play()

        # Esperar hasta que termine de reproducirse
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"Error al reproducir el archivo MP3: {e}")

    finally:
        # Detener la reproducción y cerrar pygame
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.quit()

# Ejemplo de uso:
#text = 'Hola mundo. Estamos convirtiendo texto a voz con Python.'
#mp3_file_path = text_to_speech(text)

# Llamar a la función para reproducir el archivo MP3
#reproducir_mp3(mp3_file_path)

