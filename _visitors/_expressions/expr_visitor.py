from abc import ABC
from abc import abstractmethod


class ExpressionVisitor(ABC):
    @abstractmethod
    def visit_ternary_expr(self, ternary_expr):
        raise NotImplementedError

    @abstractmethod
    def visit_assignment_expr(self, assignment_expr):
        raise NotImplementedError

    @abstractmethod
    def visit_variable_expr(self, variable_expr):
        raise NotImplementedError

    @abstractmethod
    def visit_logical_expr(self, logical_expr):
        raise NotImplementedError

    @abstractmethod
    def visit_binary_expr(self, binary_expr):
        raise NotImplementedError

    @abstractmethod
    def visit_group_expr(self, group_expr):
        raise NotImplementedError

    @abstractmethod
    def visit_literal_expr(self, literal_expr):
        raise NotImplementedError

    @abstractmethod
    def visit_unary_expr(self, unary_expr):
        raise NotImplementedError

    @abstractmethod
    def visit_call_expr(self, call_expr):
        raise NotImplementedError
