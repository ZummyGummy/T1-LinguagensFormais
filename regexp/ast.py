from tools.base import Visitee, Visitor
from dataclasses import dataclass
from abc import abstractmethod


class RegexNode(Visitee):
    pass


@dataclass
class Term(RegexNode):
    value: str

    def __repr__(self) -> str:
        return self.value if self.value else 'ε'


@dataclass
class Option(RegexNode):
    lhs: RegexNode

    def __repr__(self) -> str:
        return f'{repr(self.lhs)}?'


@dataclass
class Star(RegexNode):
    lhs: RegexNode

    def __repr__(self) -> str:
        return f'{repr(self.lhs)}*'


@dataclass
class Choice(RegexNode):
    lhs: RegexNode
    rhs: RegexNode

    def __repr__(self) -> str:
        return f'({repr(self.lhs)}|{repr(self.rhs)})'


@dataclass
class Concat(RegexNode):
    lhs: RegexNode
    rhs: RegexNode

    def __repr__(self) -> str:
        return f'({repr(self.lhs)}.{repr(self.rhs)})'


EndMarker = Term('\0')


class RegexVisitor(Visitor):

    @abstractmethod
    def visit_term(self, node: Term, *args, **kwargs):
        pass

    @abstractmethod
    def visit_concat(self, node: Concat, *args, **kwargs):
        pass

    @abstractmethod
    def visit_choice(self, node: Choice, *args, **kwargs):
        pass

    @abstractmethod
    def visit_option(self, node: Option, *args, **kwargs):
        pass

    @abstractmethod
    def visit_star(self, node: Star, *args, **kwargs):
        pass

    def generic_visit(self, node, *args, **kwargs):
        raise ValueError(node)

