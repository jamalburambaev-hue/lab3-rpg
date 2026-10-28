class UnknownCodeException(Exception):
    def __init__(self, what: str, code: str):
        super().__init__(f"{what} с кодом '{code}' не существует")
        self.what = what
        self.code = code
