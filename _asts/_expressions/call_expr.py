from _asts.visitor_interface import VisitorInterface


class Call(VisitorInterface):
    """Call node in the AST."""

    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments

    def accept(self, visitor):
        """Visitor implementation for nodes representing call expressions."""
        return visitor.visit_call_expr(self)

    def __str__(self):
        call_ast = "".join(["(calling ", str(self.callee), ")"])
        return call_ast
