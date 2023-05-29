from _callable import Callable
from _environment import Environment


class Function(Callable):
    """Creates the runtime object for a plox function."""

    MAX_PARAMS = 255

    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.name = self.declaration.get("name")
        self.params = self.declaration.get("params")
        self.body = self.declaration.get("body")
        self.line_no = self.declaration.get("line_no")
        self.closure = closure

    def arity(self):
        """Computes the number of params in a function declaration."""
        return len(self.params)

    def call(self, arguments, interpreter):
        """Calls a previously declared function. Every function call
        creates a new environment."""
        environment = Environment(self.closure)  # captures function's closure

        try:
            for param, arg in zip(self.params, arguments):
                environment.define(param.name, arg)

            interpreter.execute_block(self.body, environment)
        except Exception as e:
            # using exceptions to catch function call's return value.
            return e.value

        return None  # default return for functions w/o a return statement

    def __str__(self):
        """String representation of a plox function."""
        return "<fn {} declared on {}>".format(self.name, self.line_no)


class Return(Exception):
    """Captures function's return value."""

    def __init__(self, value):
        self.value = value
        super().__init__(self.value)
