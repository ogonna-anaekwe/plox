from _asts.visitor_interface import VisitorInterface


class Literal(VisitorInterface):
    """Literal node in the AST."""

    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        """Visitor implementation for nodes representing literal expressions."""
        return visitor.visit_literal_expr(self)

    def __str__(self):
        return str(self.value)
