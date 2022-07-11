class APIError(Exception):
    def __init__(self, desc):
        self.description = desc