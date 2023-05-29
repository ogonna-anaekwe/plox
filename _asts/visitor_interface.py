from abc import ABC
from abc import abstractmethod


class VisitorInterface(ABC):
    @abstractmethod
    def accept(self, visitor):
        NotImplementedError
