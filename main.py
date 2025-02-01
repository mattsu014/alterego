import flet as ft
import json
import re
from Gemini.main import Gemini_function
from espeak.main import voice_robot
from vosk import Model, KaldiRecognizer
import pyaudio
import os
from functions.functions import word_string
from Selenium.main import search_video
from functions.functions import get_text_after_keyword
from functions.functions import run_script
from functions.functions import add_to_json

json_path_ai = 'data/portuguese/ai.json'
json_path_user = 'data/portuguese/user.json'

modelo_path = "Vosk/vosk-model-pt-fb-v0.1.1-20220516_2113"
if not os.path.exists(modelo_path):
    raise FileNotFoundError(f"Modelo não encontrado no caminho: {modelo_path}")
model = Model(modelo_path)
rec = KaldiRecognizer(model, 16000)
def load_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: O arquivo {path} não foi encontrado.")
        return []
    except json.JSONDecodeError:
        print(f"Erro: O arquivo {path} está corrompido ou com formato inválido.")
        return []

def add_json(path, data):
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")

def extract_reaction(response):
    match = re.search(r"Reaction:\s*(\w+)", response)
    if match:
        return match.group(1).lower()
    return None

def remove_reaction_and_importance(response):
    response_without_reaction = re.sub(r"Reaction:\s*\w+", "", response)
    return response_without_reaction.strip()

def add_user(user_name, api_key, page):
    data_user = load_json(json_path_user)
    if not data_user:
        data_user.append({
            "User": user_name,
            "API_key": api_key,
            "My_history": []
        })
    else:
        data_user.append({
            "User": user_name,
            "API_key": api_key,
            "My_history": []
        })
    add_json(json_path_user, data_user)
    page.add(ft.Text(f"Usuário {user_name} cadastrado com sucesso!"))
    page.update()

def select_user(page):
    data_user = load_json(json_path_user)
    if not data_user or len(data_user) <= 1:
        page.add(ft.Text("Erro: Não há usuários cadastrados."))
        page.update()
        return None

    user_options = []
    selected_user = None

    def on_user_select(user_index):
        nonlocal selected_user
        selected_user = data_user[user_index]
        page.add(ft.Text(f"Usuário selecionado: {selected_user['User']}"))
        page.update()

    for i, user in enumerate(data_user[1:], start=1):
        user_options.append(ft.ElevatedButton(user['User'], on_click=lambda e, i=i: on_user_select(i)))

    select_button = ft.ElevatedButton("Iniciar Chat", on_click=lambda e: start_chat(page, selected_user))
    live_model_button = ft.ElevatedButton("Modelo Vivo", on_click=lambda e: start_live_chat(page, selected_user))

    page.add(ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Selecione o usuário", size=24, weight=ft.FontWeight.BOLD),
                ft.Column(user_options, alignment=ft.MainAxisAlignment.CENTER),
                select_button,
                live_model_button
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        padding=20
    ))
    page.update()

def start_chat(page, selected_user):
    if not selected_user:
        page.add(ft.Text("Nenhum usuário selecionado."))
        page.update()
        return

    page.clean()

    reaction_image = ft.Image("sprites/alterego.gif", width=1000, height=600, fit=ft.ImageFit.FILL)

    page.add(ft.Container(
        content=ft.Row(
            controls=[reaction_image], 
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=0
    ))

    response_text = ft.Text("")

    def on_send_button_click(e):
        question = question_input.value.lower()
        print(f"Pergunta: {question}")
        if question:
            if word_string("reproduzir", question) or word_string("tocar", question):
                main_answer = f"Ok, executando o comando: {question}"
                print(f"Resposta: Ok, executando o comando: {question}")
                video_name = get_text_after_keyword("reproduzir", question)
                search_video(video_name)
            if word_string("visão", question) or word_string("câmera", question):
                main_answer = "Fechando o Yolov5"
                voice_robot("Ok, executando o Yolov5, pressione a tecla q para fecha-lo")
                print(f"Resposta: Executando o Yolov5")
                run_script("Yolo/myenv", "Yolo/main.py")
            else:
                answer = Gemini_function(question, selected_user["API_key"], selected_user["User"])
                reaction = extract_reaction(answer)
                main_answer = remove_reaction_and_importance(answer)
                print(f"Reação detectada: {reaction}")
                print(f"A Pergunta foi: {question}")
                print(f"A Resposta foi {answer}")
                if reaction:
                    reaction_image.src = f"sprites/{reaction}.png"
                else:
                    reaction_image.src = "sprites/alterego.gif"
                response_text.value = f"Resposta: {main_answer}"
                question_add = {"role": "user", "parts": question}
                add_to_json("data/portuguese/ai.json", question_add)
                answer_add = {"role": "model", "parts": answer}
                add_to_json("data/portuguese/ai.json", answer_add)

            page.clean()
            page.add(ft.Container(
                content=ft.Row(
                    controls=[reaction_image], 
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                padding=0
            )) 
            voice_robot(main_answer)
            page.add(response_text)
            page.add(question_input)
            page.add(ft.Row(controls=[send_button, talk_button, exit_button], alignment=ft.MainAxisAlignment.CENTER))
            page.update()

    def on_talk_button_click(e):
        question = detectar_fala(model, rec)  
        if question:
            question_input.value = question 
            on_send_button_click(e) 

    question_input = ft.TextField(label="Digite sua pergunta")
    send_button = ft.ElevatedButton("Enviar", on_click=on_send_button_click)
    talk_button = ft.ElevatedButton("Falar", on_click=on_talk_button_click)
    exit_button = ft.ElevatedButton("Sair", on_click=lambda e: page.window_destroy())

    page.add(question_input)
    page.add(ft.Row(controls=[send_button, talk_button, exit_button], alignment=ft.MainAxisAlignment.CENTER))
    page.update()

def start_live_chat(page, selected_user):
    if not selected_user:
        page.add(ft.Text("Nenhum usuário selecionado."))
        page.update()
        return

    reaction_image = ft.Image("sprites/alterego.gif", width=1000, height=600, fit=ft.ImageFit.FILL)
    response_text = ft.Text("")

    page.clean()
    page.add(ft.Container(
        content=ft.Row(
            controls=[reaction_image],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=0
    ))
    page.add(ft.Text("Estou te escutando ☺️"))
    page.add(response_text)
    page.update()

    def listen_for_keyword():
        pa = pyaudio.PyAudio()
        stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
        stream.start_stream()

        print("Modo Vivo: Aguardando comandos com 'computador'...")
        try:
            while True:
                data = stream.read(4096, exception_on_overflow=False)
                if len(data) == 0:
                    continue

                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    detected_text = eval(result).get("text", "").lower()
                    print(f"Texto detectado: {detected_text}")
                    if detected_text.startswith("computador"):
                        stream.stop_stream()
                        stream.close()
                        pa.terminate()
                        return detected_text
        except KeyboardInterrupt:
            print("Modo Vivo interrompido.")
            stream.stop_stream()
            stream.close()
            pa.terminate()
            return None

    def process_live_interaction():
        while True:
            command = listen_for_keyword()
            if command:
                question = command.replace("computador", "").strip() 
                if question:
                    if word_string("reproduzir", question) or word_string("tocar", question):
                        video_name = get_text_after_keyword("reproduzir", question)
                        main_answer = f"Ok, reproduzindo: {video_name}"
                        reaction_image.src = f"sprites/thinking_sad.png"
                        search_video(video_name)
                    elif word_string("visão", question) or word_string("câmera", question):
                        main_answer = "YOLOv5 ativo"
                        reaction_image.src = f"sprites/happy.png"
                        voice_robot("Ok, executando o Yolov5, pressione a tecla q para fecha-lo")
                        run_script("Yolo/myenv", "Yolo/main.py")
                    elif word_string("sair", question):
                        voice_robot("ok, saindo, até logo")
                        page.window_destroy()
                    elif word_string("<unk>", question):
                        main_answer = "Desculpe, eu não consegui entender o que você disse, provavelmente está em outra lingua ou o audio está muito ruim"
                        reaction_image.src = f"sprites/thinking.png"
                    elif word_string("mateus valentim", question) or word_string("matheus valentim", question) or word_string("matheus valente", question):
                        main_answer = "Mateus Valentim é o meu criador, ele me criou baseado em uma Inteligência Artificial do jogo Danganronpa, o objetivo da minha criação é ajudar os outros e ser a sua assistente virtual. Eu sou muito grata ao Mateus por ele ter me criado"
                        reaction_image.src = f"sprites/idea.png"
                    else:
                        answer = Gemini_function(question, selected_user["API_key"], selected_user["User"])
                        reaction = extract_reaction(answer)
                        main_answer = remove_reaction_and_importance(answer)
                        if reaction:
                            reaction_image.src = f"sprites/{reaction}.png"
                        else:
                            reaction_image.src = "sprites/alterego.gif"
                        response_text.value = f"Resposta: {main_answer}"
                        question_add = {"role": "user", "parts": question}
                        add_to_json("data/portuguese/ai.json", question_add)
                        answer_add = {"role": "model", "parts": answer}
                        add_to_json("data/portuguese/ai.json", answer_add)

                    
                    response_text.value = f"Resposta: {main_answer}"
                    page.clean()
                    page.add(ft.Container(
                        content=ft.Row(
                            controls=[reaction_image],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        padding=0
                    ))
                    page.add(response_text)
                    page.update()

                    
                    voice_robot(main_answer)

    process_live_interaction()


def detectar_fala(model, rec, modelo_path="Vosk/vosk-model-pt-fb-v0.1.1-20220516_2113"):
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
    stream.start_stream()
    
    print("Fale algo (CTRL+C para sair)...")
    
    texto_detectado = ""
    try:
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if len(data) == 0:
                break
            
            if rec.AcceptWaveform(data):
                result = rec.Result()
                texto_detectado = eval(result).get("text", "")
                print(f"Você disse: {texto_detectado}")
                break
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
    
    return texto_detectado

def main(page):    
    page.title = "AlterEgo"
    page.vertical_alignment = ft.MainAxisAlignment.START

    def show_menu():
        page.clean()
        
        page.add(ft.Container(
            content=ft.Row(
                controls=[ft.Image("sprites/alterego.gif", width=1000, height=600, fit=ft.ImageFit.FILL)],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=0
        ))

        page.add(ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.ElevatedButton("Cadastrar Usuário", on_click=open_register_screen),
                            ft.ElevatedButton("Selecionar Usuário", on_click=open_select_user_screen),
                            ft.ElevatedButton("Sair", on_click=lambda e: page.window_destroy())
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=20
        ))

        page.update()

    def open_register_screen(e):
        page.clean()
        
        name_input = ft.TextField(label="Digite seu nome:")
        api_key_input = ft.TextField(label="Digite sua chave API:")
        
        def on_register_click(e):
            user_name = name_input.value
            api_key = api_key_input.value
            if user_name and api_key:
                add_user(user_name, api_key, page)
                show_menu()
            else:
                page.add(ft.Text("Por favor, insira o nome e a chave API para cadastrar."))
                page.update()

        register_button = ft.ElevatedButton("Cadastrar", on_click=on_register_click)
        page.add(name_input, api_key_input, register_button)
        page.update()

    def open_select_user_screen(e):
        page.clean()
        select_user(page)

    show_menu()

ft.app(target=main)
