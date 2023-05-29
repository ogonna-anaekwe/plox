from _asts.visitor_interface import VisitorInterface


class IfStatement(VisitorInterface):
    """IfStatement node in the AST."""

    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        """Visitor implementation for nodes representing if statements."""
        return visitor.visit_if_stmt(self)

    def __str__(self):
        if_stmt_ast = "".join(
            [
                "(if_stmt ",
                str(self.condition),
                str(self.then_branch),
                str(self.else_branch),
                ")",
            ]
        )
        return if_stmt_ast
