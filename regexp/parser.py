from typing import Optional, NoReturn
from .ast import *


class RegexParser:
    def __init__(self, source: str='') -> None:
        self.source = source
        self.current = 0
        self.__escape_sequences = {
            'n': '\n',
            'r': '\r',
            'v': '\v',
            'a': '\a',
            't': '\t',
            'f': '\f',
        }
    
    def __bool__(self) -> bool:
        return self.current < len(self.source)

    def peek(self, offset: int=0, length: int=1) -> str:
        base = self.current + offset
        return self.source[base: base + length]
    
    def advance(self, amount: int=1) -> None:
        self.current += amount
    
    def match(self, *patterns: str) -> Optional[str]:
        for pattern in patterns:
            if self.source.startswith(pattern, self.current):
                self.advance(len(pattern))
                return pattern
        return None

    def choice(self) -> RegexNode:
        lhs = self.concat()
        while self.match('|'):
            rhs = self.concat()
            lhs = Choice(lhs, rhs)
        return lhs

    def concat(self) -> RegexNode:
        lhs = self.unary()
        while self:
            if self.peek() in '|)':
                break
            rhs = self.unary()
            lhs = Concat(lhs, rhs)
        return lhs

    def unary(self) -> RegexNode:
        lhs = self.term()
        if self.match('*'):
            lhs = Star(lhs)
        elif self.match('?'):
            lhs = Option(lhs)
        return lhs

    def escape(self) -> str:
        c = self.peek()
        return self.__escape_sequences.get(c, c)

    def term(self) -> RegexNode:
        if self.match('('):
            term = self.choice()
            if not self.match(')'):
                self.err("Unbalanced parenthesis")
        elif self.match('\\'):
            term = Term(self.escape())
        elif self.match('&'):
            term = Term('')
        else:
            term = Term(self.peek())
            self.advance()
        return term

    def parse(self, regex: str) -> RegexNode:
        self.source = regex
        self.current = 0

        lhs = self.choice()
        if self:
            self.err("Something went wrong")
        return Concat(lhs, EndMarker)

    def err(self, message: str) -> NoReturn:
        raise Exception(f'Error "{message}" at:\n{self}')

    def __repr__(self) -> str:
        ws = (self.current - 1) * ' '
        return f'{self.source}\n{ws}^'

