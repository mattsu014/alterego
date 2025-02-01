#import subprocess

# def voice_robot(text):
#    subprocess.run(['espeak-ng', '-v', 'pt-br', text])

from gtts import gTTS
import os

def voice_robot(texto, idioma="pt-br"):
    tts = gTTS(text=texto, lang=idioma, slow=False)
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")  # Reproduz o arquivo de áudio (necessita do mpg321 instalado)

falar("Olá, mundo! O meu nome é MetaEgo")