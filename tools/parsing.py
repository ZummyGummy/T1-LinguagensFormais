from typing import Optional, Generic, List, Callable, Any
from abc import abstractmethod
from .token import Token, TokenType


class SyntaticError(Exception):
    pass


class BaseParser(Generic[TokenType]):
    def __init__(self, tokens: List[Token[TokenType]]):
        self.tokens: List[Token[TokenType]] = tokens
        self.current: int = 0

    def is_at_end(self, offset: int = 0):
        return self.current + offset >= len(self.tokens)

    def advance(self):
        self.current += 1

    def peek(self, offset: int = 0) -> Optional[Token[TokenType]]:
        if self.is_at_end(offset):
            # raise Exception()
            return None
        return self.tokens[self.current + offset]

    def match(self, *types: TokenType, consume=True) -> Optional[Token[TokenType]]:
        token = self.peek()
        if token and (token.token_type in types):
            self.current += 1 if consume else 0
            return token
        return None

    def err(self, message: str, err_type: type=SyntaticError) -> Exception:
        return err_type(f'Error {message} at {self.peek()}')

    def _left_associative_rule(self,
                               sub: Callable[[], Any],
                               type_: type,
                               *token_types: TokenType,
                               consume=True,
                               collect_ops=True):
        lhs = sub()
        token = self.match(*token_types, consume=consume)
        while token:
            rhs = sub()
            if collect_ops:
                lhs = type_(lhs, token, rhs)
            else:
                lhs = type_(lhs, rhs)
            token = self.match(*token_types)
        return lhs

    @staticmethod
    def __translate_token(token_t: TokenType)-> str:
        if isinstance(token_t.value, str):
            return token_t.value
        return str(token_t).split('.')[-1].lower()

    def consume(self, *types: TokenType, message: str=''):
        token = self.match(*types)
        if token:
            return token
        if message == '':
            tk = ', '.join(map(BaseParser.__translate_token, types))
            message = f'Expected {tk}'
        raise self.err(message)

    @abstractmethod
    def parse(self):
        pass
