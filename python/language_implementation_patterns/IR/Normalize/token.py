class Token:
    
    INVALID_TOKEN_TYPE = 0
    PLUS = 1
    INT = 2

    def __init__(self, type, text=None):
        self.type = type
        self.text = text

    def __str__(self):
        return str(self.text)
