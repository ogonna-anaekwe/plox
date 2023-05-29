from _asts.visitor_interface import VisitorInterface


class VariableStatement(VisitorInterface):
    """VariableStatement node in the AST."""

    def __init__(self, identifier, initializer):
        self.identifier = identifier
        self.initializer = initializer

    def accept(self, visitor):
        """Visitor implementation for nodes representing variable statements."""
        return visitor.visit_variable_stmt(self)

    def __str__(self):
        variable_stmt_ast = "".join(
            ["(", str(self.identifier), " ", str(self.initializer), ")"]
        )
        return variable_stmt_ast
