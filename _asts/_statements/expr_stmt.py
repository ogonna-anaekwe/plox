from _asts.visitor_interface import VisitorInterface


class ExpressionStatement(VisitorInterface):
    """ExpressionStatement node in the AST."""

    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        """Visitor implementation for nodes representing expression statements."""
        return visitor.visit_expression_stmt(self)

    def __str__(self):
        expr_stmt_ast = "".join(["(expr_stmt ", str(self.expression), ")"])
        return expr_stmt_ast
