from abc import abstractmethod
from abc import ABC


class Callable(ABC):
    @abstractmethod
    def arity(self):
        raise NotImplementedError

    @abstractmethod
    def call(self):
        raise NotImplementedError
