from gtts import gTTS
import os

def voice_robot(texto, idioma="pt-br"):
    try:
        tts = gTTS(text=texto, lang=idioma, slow=False)
        tts.save("output.mp3")

        # usa mpg123 (compatível com Arch)
        result = os.system("mpg123 output.mp3")

        if result != 0:
            print("⚠️ mpg123 não funcionou")

    except Exception as e:
        print("Erro na voz:", e)