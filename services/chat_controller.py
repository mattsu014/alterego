from utils.text_utils import remove_reaction, extract_reaction

class ChatController:

    def __init__(self, ai_service, voice_service, command_service):
        self.ai = ai_service
        self.voice = voice_service
        self.commands = command_service

    def handle(self, question, user):
        question = question.lower()

        # comandos
        result = self.commands.execute(question)
        if result:
            self.voice.speak(result)
            return {
                "text": result,
                "reaction": "happy"
            }

        # IA
        response = self.ai.ask(
            question,
            user["API_key"],
            user["User"]
        )

        reaction = extract_reaction(response)
        clean_text = remove_reaction(response)

        self.voice.speak(clean_text)

        return {
            "text": clean_text,
            "reaction": reaction if reaction else "alterego"
        }