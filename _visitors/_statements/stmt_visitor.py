from abc import ABC
from abc import abstractmethod


class StatementVisitor(ABC):
    @abstractmethod
    def visit_while_stmt(self, while_stmt):
        raise NotImplementedError

    @abstractmethod
    def visit_if_stmt(self, if_stmt):
        raise NotImplementedError

    @abstractmethod
    def visit_print_stmt(self, print_stmt):
        raise NotImplementedError

    @abstractmethod
    def visit_return_stmt(self, return_stmt):
        raise NotImplementedError

    @abstractmethod
    def visit_break_stmt(self, break_stmt):
        raise NotImplementedError

    @abstractmethod
    def visit_block(self, block_stmt):
        raise NotImplementedError

    @abstractmethod
    def visit_variable_stmt(self, variable_stmt):
        raise NotImplementedError

    @abstractmethod
    def visit_function_stmt(self, function_stmt):
        raise NotImplementedError

    @abstractmethod
    def visit_expression_stmt(self, expression_stmt):
        raise NotImplementedError
