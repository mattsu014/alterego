from espeak.main import voice_robot

class VoiceService:
    def speak(self, text):
        voice_robot(text)