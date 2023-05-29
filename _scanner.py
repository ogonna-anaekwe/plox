from _keywords import KEYWORDS
from _tokens._token import Token
from _tokens._token_type import TokenType


class Scanner:
    """Creates tokens from a string representation of source code."""

    def __init__(self, src):
        self.src = src
        self.start = 0
        self.current = 0
        self.line_no = 1
        self.src_len = len(self.src)
        self.tokens = []
        self.comments = []

    def scan(self):
        """Creates tokens by combining 1 or more characters."""
        while not self.at_end():
            c = self.advance()

            if c == "+":
                self.add_token(TokenType.PLUS.name)

            elif c == "-":
                self.add_token(TokenType.MINUS.name)

            elif c == "/":
                self.add_token(TokenType.SLASH.name)

            elif c == "*":
                self.add_token(TokenType.STAR.name)

            elif c == "%":
                self.add_token(TokenType.PERCENT.name)

            elif c == "^":
                self.add_token(TokenType.CARET.name)

            elif c == ">":
                self.add_token(
                    TokenType.GREATER_THAN_EQUAL.name
                    if self.match("=")
                    else TokenType.GREATER_THAN.name
                )

            elif c == "<":
                self.add_token(
                    TokenType.LESS_THAN_EQUAL.name
                    if self.match("=")
                    else TokenType.LESS_THAN.name
                )

            elif c == "=":
                self.add_token(
                    TokenType.EQUAL_EQUAL.name
                    if self.match("=")
                    else TokenType.EQUAL.name
                )

            elif c == "!":
                self.add_token(
                    TokenType.BANG_EQUAL.name
                    if self.match("=")
                    else TokenType.BANG.name
                )

            elif c == "(":
                self.add_token(TokenType.LEFT_PAREN.name)

            elif c == ")":
                self.add_token(TokenType.RIGHT_PAREN.name)

            elif c == "{":
                self.add_token(TokenType.LEFT_BRACE.name)

            elif c == "}":
                self.add_token(TokenType.RIGHT_BRACE.name)

            elif c == ";":
                self.add_token(TokenType.SEMI_COLON.name)

            elif c == ",":
                self.add_token(TokenType.COMMA.name)

            elif c == "?":
                self.add_token(TokenType.QUESTION.name)

            elif c == ":":
                self.add_token(TokenType.COLON.name)

            elif self.is_alpha(c):
                keyword = KEYWORDS.get(self.extract_identifier())
                is_keyword = keyword is not None
                self.add_token(keyword if is_keyword else TokenType.IDENTIFIER.name)

            elif c in ["'", '"']:  # allow single/double-quoted strings
                string = self.extract_string()
                str_len = len(string) - 1
                self.add_token(
                    TokenType.STRING.name,
                    literal=str(
                        string[1:str_len]
                    ),  # dropping quotes so they don't show up when concating strings with +
                )

            elif self.is_digit(c):
                digit = self.extract_digit()
                self.add_token(TokenType.NUMBER.name, literal=float(digit))

            elif c == "\n":
                self.line_no += 1
                self.proceed()

            elif c in ["\t", "\r", " "]:
                self.proceed()

            elif c == "&":
                self.add_token(TokenType.AMPERSAND.name)

            elif c == "|":
                self.add_token(TokenType.PIPE.name)

            elif c == "`":
                comment = self.extract_comment()
                self.add_comment(TokenType.BACKTICK.name, comment)
                self.proceed()

            else:
                raise TypeError(
                    "[Error on L{}]: Unexpected character {}".format(self.line_no, c),
                )

        self.add_token(TokenType.EOF.name)
        return self.tokens

    def advance(self):
        """Moves the index to the next character. Returns the previous character."""
        self.current += 1
        return self.previous()

    def previous(self):
        """Returns previous character."""
        return self.src[self.current - 1]

    def proceed(self):
        """Passes over valid characters that are not going to be made tokens."""
        self.start = self.current

    def at_end(self):
        """Validates if we've reached the end of the source code."""
        return self.current == self.src_len

    def add_token(
        self,
        type,
        literal=None,
    ):
        """Creates a Token object and appends it to the list of valid Tokens."""
        lexeme = self.src[self.start : self.current]
        self.start = self.current  # starting position of the next token.

        token = Token(type, lexeme, literal, self.line_no)
        self.tokens.append(token)

    def add_comment(self, type, literal):
        """Creates Token object and appends it to the list of comments.
        This will not be used by the Parser. However, I don't want to throw out comments!
        """
        self.comments.append(Token(type, literal, literal, self.line_no))

    def match(self, lexeme):
        """Checks if the current character matches the lexeme."""
        if self.at_end():
            return False

        lexeme_matched = self.src[self.current] == lexeme
        if lexeme_matched:
            self.advance()

        return lexeme_matched

    def peek(self):
        """Return the character one index ahead."""
        if not self.at_end():
            return self.src[self.current]

    def extract_identifier(self):
        """Captures identifiers for names: variables, functions, methods, and classes.
        Identifiers are unquoted and include alphabets (uppercase or lowercase) and underscores.
        """
        while not self.at_end() and self.is_alpha(self.peek()):
            self.advance()

        return self.src[self.start : self.current]

    def extract_digit(self):
        """Captures digits: integers or floats."""
        while not self.at_end() and (self.is_digit(self.peek()) or self.peek() == "."):
            self.advance()

        return self.src[self.start : self.current]

    def extract_string(self):
        """Captures strings: single/double-quoted."""
        empty_string = self.match("'") or self.match('"')
        if empty_string:
            raise ValueError(
                "[Error on L{}]: Can not use empty string".format(self.line_no),
            )

        while not (self.at_end() or self.peek() in ["'", '"']):
            self.advance()  # continue till end of quote. i.e end of string.

        if self.peek() in ['"', "'"]:
            self.advance()  # go past closing quote.

        matching_quotes = self.src[self.start] == self.src[self.current - 1]
        str_literal = self.src[self.start : self.current]
        if not matching_quotes:
            raise SyntaxError(
                "[Error on L{}]: Quotes do not match in {}".format(
                    self.line_no, str_literal
                ),
            )

        return str_literal

    def extract_comment(self):
        while not self.at_end() and self.peek() != "\n":
            self.advance()

        return self.src[self.start : self.current]

    def is_alpha(self, c):
        """Checks if character is an alphabet or has an underscore."""
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"

    def is_digit(self, c):
        """Checks if character is a digit."""
        return c >= "0" and c <= "9"
