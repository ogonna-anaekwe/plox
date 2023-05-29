from _asts.visitor_interface import VisitorInterface


class Unary(VisitorInterface):
    """Unary node in the AST."""

    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        """Visitor implementation for nodes representing unary expressions."""
        return visitor.visit_unary_expr(self)

    def __str__(self):
        unary_ast = "".join(["(", " ", str(self.operator), " ", str(self.right), ")"])
        return unary_ast
