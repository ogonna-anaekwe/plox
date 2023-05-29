from _tokens._token_type import TokenType

"""
Reserved for plox's use. Named objects (i.e. variables, functions, methods, and classes) 
can not be identified/named with any of these keywords.
"""
KEYWORDS = {
    "and": TokenType.AND.name,
    "break": TokenType.BREAK.name,
    "else": TokenType.ELSE.name,
    "false": TokenType.FALSE.name,
    "for": TokenType.FOR.name,
    "fun": TokenType.FUN.name,
    "if": TokenType.IF.name,
    "nil": TokenType.NIL.name,
    "or": TokenType.OR.name,
    "print": TokenType.PRINT.name,
    "return": TokenType.RETURN.name,
    "true": TokenType.TRUE.name,
    "var": TokenType.VAR.name,
    "while": TokenType.WHILE.name,
}
