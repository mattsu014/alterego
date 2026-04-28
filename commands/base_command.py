class BaseCommand:
    def match(self, text):
        raise NotImplementedError

    def execute(self, text):
        raise NotImplementedError