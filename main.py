import flet as ft
import os

# SERVICES
from services.ai_service import AIService
from services.voice_service import VoiceService
from services.command_service import CommandService
from services.chat_controller import ChatController

# IA (ESCOLHA AQUI 👇)
# from services.ollama_service import OllamaService
from services.gemini_service import GeminiService

# COMMANDS
from commands.play_command import PlayCommand

# REPOSITORY
from repositories.user_repository import UserRepository


json_path_user = 'data/portuguese/user.json'


def main(page: ft.Page):

    page.title = "AlterEgo"

    # ============================
    # 🔥 ESCOLHA DA IA AQUI
    # ============================
    # ai_service = AIService(provider=OllamaService())
    ai_service = AIService(provider=GeminiService())

    voice_service = VoiceService()

    command_service = CommandService()
    command_service.register(PlayCommand())

    controller = ChatController(
        ai_service,
        voice_service,
        command_service
    )

    repo = UserRepository(json_path_user)

    # ---------------- MENU ----------------
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
            ft.Button("Selecionar", on_click=lambda e: select_user()),
            ft.Button("Sair", on_click=lambda e: page.window_destroy())
        )

        page.update()

    # ---------------- REGISTER ----------------
    def register(e):
        page.controls.clear()

        name = ft.TextField(label="Nome")
        api = ft.TextField(label="API")

        def save(e):
            repo.add_user(name.value, api.value)
            menu()

        page.add(name, api, ft.Button("Salvar", on_click=save))
        page.update()

    # ---------------- SELECT USER ----------------
    def select_user():
        page.controls.clear()

        users = repo.load()

        for user in users:
            page.add(
                ft.Button(
                    user["User"],
                    on_click=lambda e, u=user: start_chat(u)
                )
            )

        page.update()

    # ---------------- CHAT ----------------
    def start_chat(user):
        page.controls.clear()

        img = ft.Image(
            src="sprites/alterego.gif",
            width=800,
            height=500,
            fit="fill"
        )

        txt = ft.Text("")
        input_box = ft.TextField(label="Pergunta", expand=True)

        def send(e):
            question = input_box.value

            if not question:
                txt.value = "Digite algo..."
                page.update()
                return

            result = controller.handle(question, user)

            txt.value = result["text"]

            # 🎭 troca sprite
            reaction = result["reaction"]
            path = f"sprites/{reaction}.png"

            if os.path.exists(path):
                img.src = path
            else:
                img.src = "sprites/alterego.gif"

            input_box.value = ""
            page.update()

        input_box.on_submit = send

        page.add(
            img,
            ft.Row([input_box, ft.Button("Enviar", on_click=send)]),
            txt
        )

        page.update()

    menu()


ft.app(target=main)