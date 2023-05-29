from _asts.visitor_interface import VisitorInterface


class BreakStatement(VisitorInterface):
    """BreakStatement node in the AST."""

    def __init__(self, keyword):
        self.keyword = keyword

    def accept(self, visitor):
        """Visitor implementation for nodes representing break statements."""
        return visitor.visit_break_stmt(self)
