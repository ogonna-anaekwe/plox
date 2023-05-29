from _asts.visitor_interface import VisitorInterface


class Ternary(VisitorInterface):
    """Ternary node in the AST."""

    def __init__(self, first, second, third):
        self.first = first
        self.second = second
        self.third = third

    def accept(self, visitor):
        """Visitor implementation for nodes representing ternary expressions."""
        return visitor.visit_ternary_expr(self)

    def __str__(self):
        ternary_ast = "".join(
            [
                "(",
                "(? ",
                str(self.first),
                ") (:",
                str(self.second),
                " ",
                str(self.third),
                ")",
            ]
        )
        return ternary_ast
