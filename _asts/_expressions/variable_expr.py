from _asts.visitor_interface import VisitorInterface


class Variable(VisitorInterface):
    """Variable node in the AST."""

    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        """Visitor implementation for nodes representing variable expressions."""
        return visitor.visit_variable_expr(self)

    def __str__(self):
        variable_ast = "".join(["(", str(self.name), ")"])
        return variable_ast
