from _asts.visitor_interface import VisitorInterface


class Logical(VisitorInterface):
    """Logical node in the AST."""

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        """Visitor implementation for nodes representing logical expressions."""
        return visitor.visit_logical_expr(self)

    def __str__(self):
        logical_ast = "".join(
            ["(", str(self.operator), " ", str(self.left), " ", str(self.right), ")"]
        )
        return logical_ast
