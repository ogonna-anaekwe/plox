from _asts.visitor_interface import VisitorInterface


class Assignment(VisitorInterface):
    """Assignment node in the AST."""

    def __init__(self, name, operator, value):
        self.name = name
        self.operator = operator
        self.value = value

    def accept(self, visitor):
        """Visitor implementation for nodes representing assignment expressions."""
        return visitor.visit_assignment_expr(self)

    def __str__(self):
        assignment_ast = "".join(
            [
                "(",
                str(self.operator.lexeme),
                " ",
                str(self.name),
                " ",
                str(self.value),
                ")",
            ]
        )
        return assignment_ast
