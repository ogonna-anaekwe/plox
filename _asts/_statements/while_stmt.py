from _asts.visitor_interface import VisitorInterface


class WhileStatement(VisitorInterface):
    """WhileStatement node in the AST."""

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        """Visitor implementation for nodes representing while statements."""
        return visitor.visit_while_stmt(self)

    def __str__(self):
        while_stmt_ast = "".join(
            [
                "(while_stmt ",
                str(self.condition),
                str(self.body),
                ")",
            ]
        )
        return while_stmt_ast
