from google import genai

class GeminiService:

    def ask(self, question, api_key, user):

        client = genai.Client(api_key=api_key)

        prompt = f"""
Você é uma assistente virtual inspirada no Alter Ego de Danganronpa.

Responda a pergunta de forma natural, útil e direta.

IMPORTANTE:
- Sempre finalize sua resposta com:
Reaction: <emoção>

- Escolha UMA emoção entre:
Happy, Idea, Nervous, Sad, Shocked, Talking, Thinking, Thinking_sad

Pergunta: {question}
"""

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        return response.text