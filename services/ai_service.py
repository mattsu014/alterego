class AIService:

    def __init__(self, provider):
        self.provider = provider

    def ask(self, question, api_key, user):
        return self.provider.ask(question, api_key, user)