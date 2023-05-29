from _asts.visitor_interface import VisitorInterface


class FunctionStatement(VisitorInterface):
    """FunctionStatement node in the AST."""

    def __init__(self, declaration):
        # contains function name, params (if any), and body
        self.declaration = declaration

    def accept(self, visitor):
        """Visitor implementation for nodes representing function statements."""
        return visitor.visit_function_stmt(self)

    # def __str__(self):
    #     function_stmt_ast = "".join(
    #         ["(", str(self.identifier), " ", str(self.initializer), ")"]
    #     )
    #     return function_stmt_ast
