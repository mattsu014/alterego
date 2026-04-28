class CommandService:
    def __init__(self):
        self.commands = []

    def register(self, command):
        self.commands.append(command)

    def execute(self, text):
        for command in self.commands:
            if command.match(text):
                return command.execute(text)
        return None