from commands.base_command import BaseCommand
from Selenium.main import search_video

class PlayCommand(BaseCommand):

    def match(self, text):
        return "reproduzir" in text or "tocar" in text

    def execute(self, text):
        video = get_text_after_keyword("reproduzir", text)
        search_video(video)
        return f"Tocando {video}"