class Token:
    """Defines a Token: a combination of a lexeme and literal and it's type. line_no indicates the token's position and will be used for error reporting."""

    def __init__(self, type, lexeme, literal, line_no):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line_no = line_no

    def __str__(self):
        """(Re-formats) printed tokens."""
        token = "{} {} {} L{}".format(
            self.type,
            self.lexeme,
            self.literal,
            self.line_no,
        )

        return token
