from enum import Enum
from enum import unique


@unique
class TokenType(Enum):
    """Valid types for tokens. Any token whose type isn't listed here is invalid."""

    PLUS = 0  # binary
    MINUS = 1
    SLASH = 2
    STAR = 3
    CARET = 4
    QUESTION = 5  # ternary
    PERCENT = 6  # remainder/modulo
    GREATER_THAN = 7  # comparison
    GREATER_THAN_EQUAL = 8
    LESS_THAN = 9
    LESS_THAN_EQUAL = 10
    EQUAL_EQUAL = 11  # inequality
    BANG_EQUAL = 12
    BACKTICK = 13  # comment
    EQUAL = 14  # assigment
    LEFT_PAREN = 15  # grouping/condition/call
    RIGHT_PAREN = 16
    LEFT_BRACE = 17  # blocks
    RIGHT_BRACE = 18
    BANG = 19  # unary
    NUMBER = 20  # literals and identifiers
    STRING = 21
    IDENTIFIER = 22
    COMMA = 23  # delimiters
    COLON = 24
    SEMI_COLON = 25
    FALSE = 26  # boolean
    TRUE = 27
    NIL = 28  # null/none
    FUN = 29  # function/methods
    RETURN = 30
    VAR = 31
    AND = 32  # logical
    OR = 33
    AMPERSAND = 34  # bitwise
    PIPE = 35
    PRINT = 36  # print
    FOR = 37  # loops
    WHILE = 38
    IF = 39  # branching
    ELSE = 40
    BREAK = 41  # exit loop
    EOF = 42
