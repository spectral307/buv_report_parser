from abc import ABC, abstractmethod
from .context import Context


class Expression(ABC):
    @classmethod
    @abstractmethod
    def parse(cls, context: Context):
        raise NotImplementedError()
