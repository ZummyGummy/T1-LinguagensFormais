from typing import Optional, TypeVar, Generic, Any
from enum import Enum
import os


class SourceLocation:
    def __init__(self, line: int, column: int, path: Optional[os.PathLike]=None) -> None:
        self.line: int = line
        self.column: int = column
        self.path: Optional[os.PathLike] = path

    def __repr__(self) -> str:
        pos = f'{self.line}:{self.column}'
        if self.path:
            return f'{self.path}:{pos}'
        return pos


TokenType = TypeVar('TokenType', bound=Enum)


class Token(Generic[TokenType]):
    def __init__(self, token_type: TokenType, lexeme: str, location: SourceLocation, value: Any) -> None:
        self.token_type: TokenType = token_type
        self.lexeme: str = lexeme
        self.location: SourceLocation = location
        self.value: Any = value

    def __repr__(self) -> str:
        val = f'={self.value}' if self.value else ''
        return f'<{self.token_type.name}:{self.lexeme}{val}@{self.location}>'

