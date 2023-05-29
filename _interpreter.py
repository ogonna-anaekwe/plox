from _asts._statements.while_stmt import WhileStatement
from _callable import Callable
from _environment import Environment
from _function import Function
from _function import Return
from _break import Break
from _tokens._token_type import TokenType
from _visitors._expressions.expr_visitor import ExpressionVisitor
from _visitors._statements.stmt_visitor import StatementVisitor


class Interpreter(ExpressionVisitor, StatementVisitor):
    """Interprets all AST nodes."""

    # ensures the environment persists across all instances of Interpreter
    environment = Environment()

    def __init__(self):
        pass

    def interpret(self, stmts):
        """Executes every AST node representing a statement.
        During execution, expressions contained in statements are evaluated."""
        try:
            for stmt in stmts:
                self.execute(stmt)
        except Exception as e:
            self.validate_keyword_location(stmt, e)

    def execute(self, stmt):
        """Executes statements. Statements could include expressions. As a result,
        the visitors could themselves call self.evaluate() to evaluate expressions
        contained in the statements."""
        return stmt.accept(self)

    def evaluate(self, expr):
        """Evaluates expressions."""
        return expr.accept(self)

    def visit_while_stmt(self, while_stmt):
        """Executes AST nodes for while statements. Also handles desugared for statements (if any)."""
        try:
            is_for_stmt = isinstance(while_stmt.condition, list) and isinstance(
                while_stmt.body, list
            )
            if is_for_stmt:
                # for statements are syntactic sugar for while statements.
                # so the while_stmt visitor can handle both for and while loops.
                # this branch desugars for statements.
                self.execute(while_stmt.condition[0])
                while self.is_truthy(self.evaluate(while_stmt.condition[1])):
                    for stmt in while_stmt.body:
                        self.execute(stmt)

            else:
                while self.is_truthy(self.evaluate(while_stmt.condition)):
                    self.execute(while_stmt.body)
        except Exception:
            # using exceptions to catch breaks
            pass  # what happens if i use raise?

        return None

    def visit_if_stmt(self, if_stmt):
        """Executes AST nodes for if statements."""
        condition = self.evaluate(if_stmt.condition)
        then_branch = if_stmt.then_branch
        else_branch = if_stmt.else_branch

        if self.is_truthy(condition):
            self.execute(then_branch)

        else:
            else_branch_exists = else_branch is not None
            if else_branch_exists:
                self.execute(else_branch)

        return None

    def visit_print_stmt(self, print_stmt):
        """Executes AST nodes for print statements."""
        value = self.evaluate(print_stmt.expression)
        print(value)
        return None

    def visit_return_stmt(self, return_stmt):
        """Executes AST nodes for return statements."""
        value = return_stmt.expression
        if value is not None:
            value = self.evaluate(return_stmt.expression)

        # caught during function call wherein we grab the value and return that.
        raise Return(value)

    def visit_break_stmt(self, break_stmt):
        raise Break(break_stmt.keyword)

    def visit_block(self, block):
        """Executes AST nodes for statements contained within blocks."""
        self.execute_block(block.statements, Environment(Interpreter.environment))
        return None

    def execute_block(self, statements, enclosing):
        """Executes all statements that are within a block.
        Each new block has its own environment which itself has its own enclosing."""
        preceding_environment = enclosing  # Save environment containing the block. Will be restored after the block

        try:
            # statements in a block are executed in a new environment which itself has an enclosing environment.
            Interpreter.environment = enclosing
            for stmt in statements:
                self.execute(stmt)

        except Exception:
            raise

        finally:
            # discard environment upon exiting the owning block.
            Interpreter.environment = preceding_environment

    def visit_variable_stmt(self, variable_stmt):
        """Executes AST nodes for variable statements/declarations."""
        identifier = variable_stmt.identifier.lexeme
        is_initialized = variable_stmt.initializer is not None
        initializer = (
            self.evaluate(variable_stmt.initializer)
            if is_initialized
            else variable_stmt.initializer
        )

        Interpreter.environment.define(identifier, initializer)
        return None

    def visit_function_stmt(self, function_stmt):
        """Executes AST nodes for function statements i.e. declarations."""
        name = function_stmt.declaration.get("name")
        num_params = len(function_stmt.declaration.get("params"))
        max_params = Function.MAX_PARAMS
        if num_params > max_params:
            raise ValueError(
                "Too many params in the {} function. Max params: {}.".format(
                    name, max_params
                )
            )

        function = Function(function_stmt.declaration, Interpreter.environment)
        Interpreter.environment.define(name, function)
        return None

    def visit_expression_stmt(self, expression_stmt):
        """Executes AST nodes for expression statements. These are expressions contained in statements."""
        self.evaluate(expression_stmt.expression)
        return None

    def visit_ternary_expr(self, ternary_expr):
        """Executes AST nodes for ternary expressions."""
        first = self.evaluate(ternary_expr.first)

        if self.is_truthy(first):
            return self.evaluate(ternary_expr.second)

        return self.evaluate(ternary_expr.third)

    def visit_assignment_expr(self, assignment_expr):
        name, value = assignment_expr.name, self.evaluate(assignment_expr.value)
        Interpreter.environment.assign(name, value)

        # return value instead of None.
        # This guarantees that for multiple assignment: a = b = 1, all identifiers get value rather than None.
        # Otherwise, only the last identifier gets value with the rest set to None.
        return value

    def visit_variable_expr(self, variable_expr):
        """Evaluates AST nodes for variable expressions.
        Applies to declared identifiers/names used in expressions: variable names, function names
        """
        return Interpreter.environment.get(variable_expr.name)

    def visit_logical_expr(self, logical_expr):
        """Evaluates AST nodes for logical expressions."""
        left = self.evaluate(logical_expr.left)
        right = logical_expr.right
        operator = logical_expr.operator.type

        if operator == TokenType.OR.name:
            if self.is_truthy(left):
                return left
            else:
                right = self.evaluate(right)
                if self.is_truthy(right):
                    return right

            return False

        if operator == TokenType.AND.name:
            if not self.is_truthy(left):
                return False

            right = self.evaluate(right)
            if self.is_truthy(right):
                return left

            return False

    def visit_binary_expr(self, binary_expr):
        """Evaluates AST nodes for binary expressions."""
        left = self.evaluate(binary_expr.left)
        right = self.evaluate(binary_expr.right)
        operator = binary_expr.operator.type
        line_no = binary_expr.operator.line_no

        if operator == TokenType.PIPE.name:
            self.check_operands(line_no, left, right)
            return int(left) | int(right)  # bitwise operators work on integers only.

        if operator == TokenType.AMPERSAND.name:
            self.check_operands(line_no, left, right)
            return int(left) & int(right)  # bitwise operators work on integers only.

        if operator == TokenType.PLUS.name:
            if self.either_float_or_str(left, right):
                left, right = self.cast_to_int(left), self.cast_to_int(right)
                return str(left) + str(right)

            else:
                if self.both_float_or_str(line_no, left, right):
                    return left + right

        if operator == TokenType.MINUS.name:
            self.check_operands(line_no, left, right)
            return left - right

        if operator == TokenType.SLASH.name:
            self.check_operands(line_no, left, right)
            self.check_zero_div(line_no, right)
            return left / right

        if operator == TokenType.STAR.name:
            self.check_operands(line_no, left, right)
            return left * right

        if operator == TokenType.PERCENT.name:
            self.check_operands(line_no, left, right)
            return left % right

        if operator == TokenType.BANG_EQUAL.name:
            self.check_operands(line_no, left, right)
            return not self.is_equal(left, right)

        if operator == TokenType.EQUAL_EQUAL.name:
            self.check_operands(line_no, left, right)
            return self.is_equal(left, right)

        if operator == TokenType.GREATER_THAN.name:
            if self.both_float_or_str(line_no, left, right):
                return left > right

        if operator == TokenType.GREATER_THAN_EQUAL.name:
            if self.both_float_or_str(line_no, left, right):
                return left >= right

        if operator == TokenType.LESS_THAN.name:
            if self.both_float_or_str(line_no, left, right):
                return left < right

        if operator == TokenType.LESS_THAN_EQUAL.name:
            if self.both_float_or_str(line_no, left, right):
                return left <= right

        if operator == TokenType.CARET.name:
            return pow(left, right)

    def visit_group_expr(self, group_expr):
        """Evaluates AST nodes for group expressions."""
        return self.evaluate(group_expr.expression)

    def visit_literal_expr(self, literal_expr):
        """Evaluates AST nodes for literals expressions. We just return the literal value."""
        return literal_expr.value

    def visit_unary_expr(self, unary_expr):
        """Evaluates AST nodes for unary expressions."""
        right = self.evaluate(unary_expr.right)
        operator = unary_expr.operator.type

        if operator == TokenType.BANG.name:
            return not self.is_truthy(right)

        if operator == TokenType.MINUS.name:
            self.check_operands(right)
            return -right

    def visit_call_expr(self, call_expr):
        """Evaluates AST nodes for function call expressions."""
        callee = self.evaluate(call_expr.callee)
        is_callable = isinstance(callee, Callable)
        if not is_callable:
            raise TypeError("Can't call object of type {}".format(type(callee)))

        arguments = []
        for argument in call_expr.arguments:
            arguments.append(self.evaluate(argument))

        arity_pass = callee.arity() == len(arguments)
        if not arity_pass:
            raise ValueError(
                "Parameters declared do not match arguments passed in {}".format(callee)
            )

        # we need some methods from the interpreter object in the function.
        # we pass the interpreter as the first argument via self for this reason.
        return callee.call(arguments, self)

    def check_operands(self, line_no, *operands):
        """Checks the type of operand. Operands' types must be valid for the operator type."""
        num_operands = len(operands)
        is_binary = num_operands == 2
        is_unary = num_operands == 1

        if is_binary:
            left, right = operands[0], operands[1]
            both_floats = isinstance(left, float) and isinstance(right, float)
            if not both_floats:
                raise TypeError(
                    "[Error on L{}]: Operands must be float".format(line_no)
                )

        if is_unary:
            right = operands[0]
            is_float = isinstance(right, float)
            if not is_float:
                raise TypeError(
                    "[Error on L{}]: Operand must be float.".format(line_no)
                )

    def both_float_or_str(self, line_no, *operands):
        """Checks that both operands are both float or both str."""
        left, right = operands[0], operands[1]
        both_floats = isinstance(left, float) and isinstance(right, float)
        both_strings = isinstance(left, str) and isinstance(right, str)
        same_type = both_floats or both_strings

        if not same_type:
            raise TypeError(
                [
                    "[Error on L{}]: Operands must be both float or both str.".format(
                        line_no
                    )
                ]
            )

        return True

    def either_float_or_str(self, *operands):
        """Checks that 1 operand is float and the other str or vice versa."""
        left, right = operands[0], operands[1]

        return (isinstance(left, float) and isinstance(right, str)) or (
            isinstance(left, str) and isinstance(right, float)
        )

    def cast_to_int(self, operand):
        """Python converts str(<int>.0) to "<int>.0". This method drops the fractional part."""
        if isinstance(operand, float) and operand % 1 == 0:
            return int(operand)

        return operand

    def check_zero_div(self, line_no, right):
        if right == 0:
            raise ValueError("[Error on L{}]: Can't divide by zero".format(line_no))

    def is_truthy(self, operand):
        if operand == 0 or operand is None:
            return False

        if isinstance(operand, bool):
            return operand

        return True

    def is_equal(self, left, right):
        if left is None and right is None:
            return True

        if left is None:
            return False

        return left == right

    def validate_keyword_location(self, stmt, exception):
        keyword_exists = exception.keyword is not None
        if keyword_exists:
            if exception.keyword.lexeme == "break":
                if isinstance(stmt, WhileStatement):
                    pass
                else:
                    raise SyntaxError(
                        "[Error on L{}]: Can't use break outside loop.".format(
                            exception.keyword.line_no
                        )
                    )
