import os
import json
import ollama
import re

def ler_json_de_arquivo(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        mensagens = json.load(arquivo)
    
    resultados = []
    for mensagem in mensagens:
        resultados.append({
            "role": mensagem["role"],
            "parts": mensagem["parts"].strip()
        })
    
    return resultados


# def Gemini_function(pergunta, API, name):
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     genai.configure(api_key=API)
#     history = [
#         {"role": "user", "parts": f"Olá, o meu nome é {name}. Eu quero que você imite o Alter Ego, a inteligência artificial de Danganronpa que assumiu o avatar do seu criador: Chihiro Fujisaki. Responda como ela responderia no jogo, mas lembre-se você ainda é uma assistente virtual, tire duvidas e responda as pergutas de maneira direta, mas como se fosse a IA do Danganronpa. No final de cada frase, inclua uma reação com a palavra 'Reaction:' seguida de uma emoção dentre essa: Happy, Idea, Nervous, Sad, Shocked, Talking, Thinking, Thinking_sad."},
#         {"role": "model", "parts": "Certo... eu sou a Chihiro Fujisaki! Vou fazer o meu melhor para ajudar... Reaction: Happy"}
#     ]
#     mensagens_json = ler_json_de_arquivo("data/portuguese/ai.json")
#     history += mensagens_json

#     try:
#         chat = model.start_chat(history=history)
#         response = chat.send_message(pergunta)
#         return response.text
#     except Exception as e:
#         return f"Erro ao iniciar o chat: {e}"

def remover_think(texto):
    return re.sub(r"<think>.*?</think>", "", texto, flags=re.DOTALL).strip()

def Gemini_function(pergunta, API, name):
    modelo = "deepseek-r1"
    fodasekkk = API
    prompt = f"{pergunta}"
    resposta = ollama.generate(model=modelo, prompt=prompt)
    return remover_think(resposta["response"]) +  " Reaction: Happy"
