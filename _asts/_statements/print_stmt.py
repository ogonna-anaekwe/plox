from _asts.visitor_interface import VisitorInterface


class PrintStatement(VisitorInterface):
    """PrintStatement node in the AST."""

    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        """Visitor implementation for nodes representing print statements."""
        return visitor.visit_print_stmt(self)

    def __str__(self):
        print_stmt_ast = "".join(["(print ", str(self.expression), ")"])
        return print_stmt_ast
