import ollama
import re

def remover_think(texto):
    return re.sub(r"<think>.*?</think>", "", texto, flags=re.DOTALL).strip()

class OllamaService:

    def ask(self, question, api_key, user):
        resposta = ollama.generate(
            model="deepseek-r1",
            prompt=question
        )

        return remover_think(resposta["response"]) + " Reaction: Happy"