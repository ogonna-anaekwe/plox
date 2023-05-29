from _asts.visitor_interface import VisitorInterface


class Binary(VisitorInterface):
    """Binary node in the AST."""

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        """Visitor implementation for nodes representing binary expressions."""
        return visitor.visit_binary_expr(self)

    def __str__(self):
        binary_ast = "".join(
            ["(", str(self.operator), " ", str(self.left), " ", str(self.right), ")"]
        )
        return binary_ast
