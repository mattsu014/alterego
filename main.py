import flet as ft
import json
import re
from Gemini.main import Gemini_function
from espeak.main import voice_robot
from vosk import Model, KaldiRecognizer
import pyaudio
import os
from Selenium.main import search_video
from functions.functions import get_text_after_keyword

json_path_user = 'data/portuguese/user.json'

modelo_path = "Vosk/vosk-model-pt-fb-v0.1.1-20220516_2113"
model = Model(modelo_path)
rec = KaldiRecognizer(model, 16000)


def load_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return []


def add_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


def extract_reaction(response):
    match = re.search(r"Reaction:\s*(\w+)", response)
    return match.group(1).lower() if match else None


def remove_reaction(response):
    return re.sub(r"Reaction:\s*\w+", "", response).strip()


def add_user(user_name, api_key, page):
    data = load_json(json_path_user)

    data.append({
        "User": user_name,
        "API_key": api_key
    })

    add_json(json_path_user, data)

    page.snack_bar = ft.SnackBar(ft.Text("Usuário cadastrado!"))
    page.snack_bar.open = True
    page.update()


def select_user(page):
    data = load_json(json_path_user)

    page.controls.clear()
    page.add(ft.Text("Selecione o usuário"))

    for user in data:
        page.add(
            ft.Button(
                user["User"],
                on_click=lambda e, u=user: start_chat(page, u)
            )
        )

    page.update()


def start_chat(page, user):
    page.controls.clear()

    img = ft.Image(
        src="sprites/alterego.gif",
        width=800,
        height=500,
        fit="fill"
    )

    txt = ft.Text(value="")

    input_box = ft.TextField(
        label="Pergunta",
        expand=True
    )

    def send(e):
        question = input_box.value

        if not question:
            txt.value = "Digite algo primeiro..."
            page.update()
            return

        question = question.lower()
        print("BOTÃO FUNCIONANDO:", question)

        try:
            if "reproduzir" in question:
                video = get_text_after_keyword("reproduzir", question)
                search_video(video)
                resposta = f"Tocando {video}"
            else:
                r = Gemini_function(
                    question,
                    user["API_key"],
                    user["User"]
                )
                resposta = remove_reaction(r)

        except Exception as err:
            resposta = f"Erro: {err}"
            print(err)

        txt.value = resposta
        input_box.value = ""

        voice_robot(resposta)

        page.update()

    # ENTER para enviar
    input_box.on_submit = send

    btn = ft.Button("Enviar", on_click=send)

    page.add(
        img,
        ft.Row([input_box, btn]),
        txt
    )

    page.update()


def main(page: ft.Page):
    page.title = "AlterEgo"

    def menu():
        page.controls.clear()

        page.add(
            ft.Image(
                src="sprites/alterego.gif",
                width=800,
                height=500,
                fit="fill"
            )
        )

        page.add(
            ft.Button("Cadastrar", on_click=register),
            ft.Button("Selecionar", on_click=lambda e: select_user(page)),
            ft.Button("Sair", on_click=lambda e: page.window_destroy())
        )

        page.update()

    def register(e):
        page.controls.clear()

        name = ft.TextField(label="Nome")
        api = ft.TextField(label="API")

        def save(e):
            add_user(name.value, api.value, page)
            menu()

        page.add(
            name,
            api,
            ft.Button("Salvar", on_click=save)
        )

        page.update()

    menu()


ft.run(main)