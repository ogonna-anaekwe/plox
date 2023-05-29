from _asts.visitor_interface import VisitorInterface


class Block(VisitorInterface):
    """BlockStatement node in the AST."""

    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        """Visitor implementation for nodes representing blocks."""
        return visitor.visit_block(self)

    def __str__(self):
        block_ast = "".join(["(block ", str(self.statements), ")"])
        return block_ast
