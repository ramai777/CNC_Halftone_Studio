from config import Settings


class Project:

    def __init__(self):

        self.settings = Settings()

        self.filename = None

        self.image = None

        self.preview = None

        self.holes = []