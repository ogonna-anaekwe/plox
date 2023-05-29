from _asts._expressions.assign_expr import Assignment
from _asts._expressions.binary_expr import Binary
from _asts._expressions.call_expr import Call
from _asts._expressions.group_expr import Group
from _asts._expressions.literal_expr import Literal
from _asts._expressions.logical_expr import Logical
from _asts._expressions.ternary_expr import Ternary
from _asts._expressions.unary_expr import Unary
from _asts._expressions.variable_expr import Variable
from _asts._statements.block import Block
from _asts._statements.break_stmt import BreakStatement
from _asts._statements.expr_stmt import ExpressionStatement
from _asts._statements.fun_stmt import FunctionStatement
from _asts._statements.if_stmt import IfStatement
from _asts._statements.print_stmt import PrintStatement
from _asts._statements.return_stmt import ReturnStatement
from _asts._statements.var_stmt import VariableStatement
from _asts._statements.while_stmt import WhileStatement
from _tokens._token_type import TokenType


class Parser:
    """Creates the AST nodes from the list of tokens emitted by the Scanner."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        """Creates valid AST nodes from list of tokens."""
        asts = []
        while not self.at_end():
            ast = self.declaration()
            asts.append(ast)

        return asts

    def declaration(self):
        """Creates AST nodes for declarations and statements."""
        try:
            if self.match(TokenType.VAR.name):
                return self.var_declaration()

            if self.match(TokenType.FUN.name):
                return self.fun_declaration()

            return self.statement()
        except:
            self.synchronize()

    def var_declaration(self):
        """Creates AST node for variable declarations/definitions."""
        identifier = self.consume(
            TokenType.IDENTIFIER.name, "Missing variable name in variable statement."
        )
        initializer = None
        if self.match(TokenType.EQUAL.name):
            initializer = self.expression()
        self.consume(TokenType.SEMI_COLON.name, "Missing ';' in variable statement.")

        return VariableStatement(identifier, initializer)

    def fun_declaration(self):
        name = self.consume(
            TokenType.IDENTIFIER.name, "Missing function name in function declaration."
        )

        self.consume(
            TokenType.LEFT_PAREN.name, "Missing opening '(' in function parameter."
        )

        params = []

        if not self.match(TokenType.RIGHT_PAREN.name):
            param = self.expression()
            params.append(param)
            while self.match(TokenType.COMMA.name):
                param = self.expression()
                params.append(param)

            self.consume(
                TokenType.RIGHT_PAREN.name, "Missing closing ')' in function parameter."
            )

        self.consume(TokenType.LEFT_BRACE.name, "Missing opening '{' in function body.")
        body = self.block()

        declaration = {
            "name": name.lexeme,
            "params": params,
            "body": body.statements,
            "line_no": name.line_no,
        }

        return FunctionStatement(declaration)

    def statement(self):
        """Creates AST nodes for all statement types: for, while, if, print, blocks, etc."""
        if self.match(TokenType.FOR.name):
            return self.for_statement()

        if self.match(TokenType.WHILE.name):
            return self.while_statement()

        if self.match(TokenType.IF.name):
            return self.if_statement()

        if self.match(TokenType.PRINT.name):
            return self.print_statement()

        if self.match(TokenType.RETURN.name):
            return self.return_statement()

        if self.match(TokenType.BREAK.name):
            return self.break_statement()

        if self.match(TokenType.LEFT_BRACE.name):
            return self.block()

        return self.expression_statement()

    def for_statement(self):
        """Desugars 'for statement' (which is syntactic sugar for a 'while statement') by converting
        it to an AST node for a while statement."""
        self.consume(TokenType.LEFT_PAREN.name, "Missing opening '(' in for statement.")

        initializer = Literal(None)
        condition = Literal(True)  # means an infinite while loop
        update = Literal(None)

        if not self.match(TokenType.SEMI_COLON.name):
            initializer = (
                self.var_declaration()
                if self.match(TokenType.VAR.name)
                else self.expression_statement()
            )

        if not self.match(TokenType.SEMI_COLON.name):
            condition = self.expression()
            self.consume(TokenType.SEMI_COLON.name, "Missing ';' in for statement.")

        if not self.match(TokenType.RIGHT_PAREN.name):
            update = self.expression()
            self.consume(
                TokenType.RIGHT_PAREN.name, "Missing closing ')' in for statement."
            )

        body = self.statement()
        condition_list = [initializer, condition]
        body_list = [body, update]

        return WhileStatement(condition_list, body_list)

    def while_statement(self):
        """Creates AST node for while statements."""
        self.consume(
            TokenType.LEFT_PAREN.name, "Missing opening '(' in while condition."
        )
        condition = self.expression()
        self.consume(
            TokenType.RIGHT_PAREN.name, "Missing closing ')' in while condition."
        )
        body = self.statement()

        return WhileStatement(condition, body)

    def if_statement(self):
        """Creates AST node for if statements."""
        self.consume(TokenType.LEFT_PAREN.name, "Missing opening '(' in if condition.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN.name, "Missing closing ')' in if condition.")

        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE.name):
            else_branch = self.statement()

        return IfStatement(condition, then_branch, else_branch)

    def print_statement(self):
        """Creates AST node for print statements."""
        expr = self.expression()
        self.consume(TokenType.SEMI_COLON.name, "Missing ';' in print statement.")
        return PrintStatement(expr)

    def return_statement(self):
        """Creates AST node for return statements."""
        expr = None
        if not self.match(TokenType.SEMI_COLON.name):
            expr = self.expression()
            self.consume(TokenType.SEMI_COLON.name, "Missing ';' in print statement.")

        return ReturnStatement(expr)

    def break_statement(self):
        keyword = self.previous()
        self.consume(TokenType.SEMI_COLON.name, "Missing ';' in print statement.")
        return BreakStatement(keyword)

    def block(self):
        """Creates AST node for blocks."""
        block_stmts = []
        while not (self.at_end() or self.match(TokenType.RIGHT_BRACE.name)):
            block_stmt = self.declaration()
            block_stmts.append(block_stmt)

        self.current -= 1  # gives the closing } for the check below.
        self.consume(TokenType.RIGHT_BRACE.name, "Missing closing '}' in block.")

        return Block(block_stmts)

    def expression_statement(self):
        """Creates AST node for expression statements i.e. expressions followed by a semi colon."""
        expr = self.expression()
        self.consume(TokenType.SEMI_COLON.name, "Missing ';' in expression statement.")
        return ExpressionStatement(expr)

    def expression(self):
        """Creates AST node for expressions."""
        return self.ternary()

    def ternary(self):
        """Creates AST node for ternary expressions."""
        expr = self.assignment()

        while self.match(TokenType.QUESTION.name):
            second = self.ternary()
            self.consume(TokenType.COLON.name, "Missing ':' in ternary expression.")
            third = self.ternary()
            expr = Ternary(expr, second, third)

        return expr

    def assignment(self):
        """Creates AST node for assignment expressions."""
        expr = self.logical_or()

        while self.match(TokenType.EQUAL.name):
            operator = self.previous()
            # calling self.ternary to assign a ternary to a variable
            # or use a ternary as an expression statement.
            # replace with self.assignment() and see what happens.
            value = self.ternary()  # right-associative.

            if isinstance(expr, Variable):
                name = expr.name
                return Assignment(name, operator, value)

            raise ValueError("Invalid assignment target")

        return expr

    def logical_or(self):
        """Creates AST node for logical OR expressions."""
        expr = self.logical_and()

        while self.match(TokenType.OR.name):
            operator = self.previous()
            right = self.logical_and()
            expr = Logical(expr, operator, right)

        return expr

    def logical_and(self):
        """Creates AST node for logical AND expressions."""
        expr = self.bitwise_or()

        while self.match(TokenType.AND.name):
            operator = self.previous()
            right = self.bitwise_or()
            expr = Logical(expr, operator, right)

        return expr

    def bitwise_or(self):
        """Creates AST node for bitwise OR expressions."""
        expr = self.bitwise_and()

        while self.match(TokenType.PIPE.name):
            operator = self.previous()
            right = self.bitwise_and()
            expr = Binary(expr, operator, right)

        return expr

    def bitwise_and(self):
        """Creates AST node for bitwise AND expressions."""
        expr = self.equality()

        while self.match(TokenType.AMPERSAND.name):
            operator = self.previous()
            right = self.equality()
            expr = Binary(expr, operator, right)

        return expr

    def equality(self):
        """Creates AST node for equality expressions."""
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL.name, TokenType.EQUAL_EQUAL.name):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self):
        """Creates AST node for comparison expressions."""
        expr = self.term()

        while self.match(
            TokenType.GREATER_THAN.name,
            TokenType.GREATER_THAN_EQUAL.name,
            TokenType.LESS_THAN.name,
            TokenType.LESS_THAN_EQUAL.name,
        ):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        """Creates AST node for term expressions."""
        expr = self.factor()

        while self.match(TokenType.PLUS.name, TokenType.MINUS.name):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        """Creates AST node for factor expressions."""
        expr = self.unary()

        while self.match(
            TokenType.SLASH.name, TokenType.STAR.name, TokenType.PERCENT.name
        ):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        """Creates AST node for unary expressions."""
        while self.match(TokenType.BANG.name, TokenType.MINUS.name):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.power()

    def power(self):
        """Creates AST node for exponentiation/power expressions."""
        expr = self.call()

        while self.match(TokenType.CARET.name):
            operator = self.previous()
            right = self.power()
            return Binary(expr, operator, right)

        return expr

    def call(self):
        """Creates AST node for function call expressions."""
        expr = self.primary()

        while self.match(TokenType.LEFT_PAREN.name):
            args = []
            if not self.match(TokenType.RIGHT_PAREN.name):
                arg = self.expression()
                args.append(arg)
                while self.match(TokenType.COMMA.name):
                    arg = self.expression()
                    args.append(arg)

                self.consume(
                    TokenType.RIGHT_PAREN.name, "Missing closing ')' in function call."
                )

            expr = Call(expr, args)

        return expr

    def primary(self):
        """Creates AST node for primary expressions i.e. terminals."""
        if self.match(TokenType.NUMBER.name):
            return Literal(self.previous().literal)

        if self.match(TokenType.STRING.name):
            return Literal(self.previous().literal)

        if self.match(TokenType.TRUE.name):
            return Literal(True)

        if self.match(TokenType.FALSE.name):
            return Literal(False)

        if self.match(TokenType.NIL.name):
            return Literal(None)

        if self.match(TokenType.LEFT_PAREN.name):
            expr = self.expression()
            self.consume(
                TokenType.RIGHT_PAREN.name, "Missing closing ')' in group expression."
            )
            return Group(expr)

        if self.match(TokenType.IDENTIFIER.name):
            name = self.previous().lexeme
            return Variable(name)

        raise TypeError("Expected expression.")

    def advance(self):
        """Increments token index and return the previous token."""
        if not self.at_end():
            self.current += 1

        return self.previous()

    def previous(self):
        """Returns the previous token."""
        return self.tokens[self.current - 1]

    def current_token_type(self):
        """Returns the current token's type."""
        return self.tokens[self.current].type

    def match(self, *token_types):
        """Validates if one/more tokens type match the current token's type.
        Advances to the next token there is a match."""
        for token_type in token_types:
            type_match = self.current_token_type() == token_type
            if type_match:
                self.advance()
                return True

        return False

    def consume(self, token_type, message):
        """Similar to self.match, except this checks a single token type and is used for syntax checks."""
        type_match = self.current_token_type() == token_type
        if type_match:
            return self.advance()

        raise TypeError("[Error on L{}]: {}".format(self.previous().line_no, message))

    def at_end(self):
        """Validates if we've reached the end of token list."""
        return self.tokens[self.current].type == TokenType.EOF.name

    def synchronize(self):
        self.advance()

        while not self.at_end():
            if self.previous().type == TokenType.SEMI_COLON.name:
                return

            if self.tokens[self.current].type in [
                TokenType.FOR.name,
                TokenType.FUN.name,
                TokenType.IF.name,
                TokenType.PRINT.name,
                TokenType.RETURN.name,
                TokenType.VAR.name,
                TokenType.WHILE.name,
            ]:
                return

            self.advance()
