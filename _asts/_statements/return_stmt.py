from _asts.visitor_interface import VisitorInterface


class ReturnStatement(VisitorInterface):
    """ReturnStatement node in the AST."""

    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        """Visitor implementation for nodes representing return statements."""
        return visitor.visit_return_stmt(self)

    def __str__(self):
        return_stmt_ast = "".join(["(return ", str(self.expression), ")"])
        return return_stmt_ast
