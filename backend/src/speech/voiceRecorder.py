import pyaudio
import wave
import speech_recognition as sr


##Channels: 1 : Para conectar con el micro del casco A
class voiceRecorder:
    def __init__(self, chunk=1024, sample_format=pyaudio.paInt16, channels=1, fs=44100, file="test.wav"):
        self.chunk = chunk
        self.sample_format = sample_format
        self.channels = channels
        self.fs = fs
        self.file = file
        self.p = pyaudio.PyAudio()  # Crear una interfaz a PyAudio

    def record(self):
        print('Grabando')
        print('Presiona Ctrl+C para detener la grabación.')

        stream = self.p.open(format=self.sample_format,
                             channels=self.channels,
                             rate=self.fs,
                             frames_per_buffer=self.chunk,
                             input=True)

        frames = []  # Inicializar array para almacenar frames

        try:
            while True:
                data = stream.read(self.chunk)
                frames.append(data)
                print('.', end='', flush=True)  # Imprimir un punto mientras se graba

        except KeyboardInterrupt:
            pass  # Se interrumpe manualmente con Ctrl+C

        # Detener y cerrar el stream
        stream.stop_stream()
        stream.close()
        # Terminar la interfaz de PyAudio
        self.p.terminate()
        print('\nGrabación finalizada')
        # Abrir archivo de voz
        wf = wave.open(self.file, 'wb')
        # Establecer canales
        wf.setnchannels(self.channels)
        # Establecer formato
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        # Establecer frecuencia de muestreo
        wf.setframerate(self.fs)
        # Guardar
        wf.writeframes(b''.join(frames))
        wf.close()

# TEST (grabación hasta que se presiona Ctrl+C)
recorder = voiceRecorder()
recorder.record()

