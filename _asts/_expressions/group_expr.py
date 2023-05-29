from _asts.visitor_interface import VisitorInterface


class Group(VisitorInterface):
    """Group node in the AST."""

    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        """Visitor implementation for nodes representing group/parenthesized expressions."""
        return visitor.visit_group_expr(self)

    def __str__(self):
        group_ast = "".join(["(group ", str(self.expression), ")"])
        return group_ast
