from .token import TokenType, Token, SourceLocation
from typing import Generic, List, Any, Optional
from abc import abstractmethod


class LexicalError(Exception):
    pass


class BaseLexer(Generic[TokenType]):
    """
        Base class for all lexers, keeps track of
        the current state during the lexing process,
        allowing unlimited lookahead and lookbehind,
        simple pattern matching and error reporting
    """
    def __init__(self, source: str) -> None:
        self.source: str = source
        self.current: int = 0
        self.lexeme_start: int = 0
        self.line_start: int = 0
        self.line: int = 1
        self.tokens: List[Token[TokenType]] = []
        self._unvalued_tokens = None

    @property
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def peek(self, offset: int = 0, length: int = 1) -> str:
        """
        Allows look-around and slicing using as base position the current character

        :param offset: signed offset from the current character
        :type offset: int
        :param length: the length of the slice, the default is 1
        :type length: int
        :return:
            String containing the selected characters. Since it uses a string slice
            it never throws exceptions, when the arguments are invalid
            or the lexer is at the end of the source an empty string is returned
        :rtype: str
        """
        base = self.current + offset
        return self.source[base:base + length]

    def advance(self, amount: int = 1) -> str:
        """
        Advances the current position of the lexer
        :param amount: the amount of characters to advance, the default is 1
        :type amount: int
        :return:
            After advancing the lexer peeks back and returns the resulting string
        :rtype: str
        """
        self.current += amount
        return self.peek(-amount, amount)

    def sync(self) -> None:
        """
        Synchronizes the lexeme start with the current character,
        can be used to skip characters or lexemes
        ex:
        >>> lexer = BaseLexer('test')
        >>> lexer.advance(2)
        'te'
        >>> print(lexer)
        test
        ^^^
        >>> lexer.sync()
        >>> print(lexer)
        test
        --^
        :rtype: None
        """
        self.lexeme_start = self.current

    def __repr__(self) -> str:
        """
        Returns the lexer state as a string
        :return: the lexer state
        :rtype: str
        """
        eol_pos = self.source.find('\n', self.line_start)
        if eol_pos >= 0:
            line = self.source[self.line_start:eol_pos]
        else:
            line = self.source[self.line_start:]
        pointer = '-' * (self.lexeme_start - self.line_start)
        pointer += '^' * (self.current - self.lexeme_start + 1)
        return f'{line}\n{pointer}'

    def here(self, lexeme_wise: bool = True) -> SourceLocation:
        """
        Returns the current location of the lexer
        :param lexeme_wise:
            if True returns the location based on the lexeme start,
            otherwise returns the location based on the current character
        :type lexeme_wise: bool
        :return:
            The location
        :rtype: SourceLocation
        """
        column = (self.lexeme_start if lexeme_wise else self.current) - self.line_start
        return SourceLocation(self.line, column)

    def err(self, message: str) -> LexicalError:
        """
        Returns a LexicalError exception with the given message and
        the current lexer state
        :param message: error message
        :type message: str
        :return: error to be raised
        :rtype: LexicalError
        """
        result = f'Error "{message}" at {self.here(False)}:\n{self}'
        return LexicalError(result)

    def match(self, *patterns: str) -> Optional[str]:
        """
        Tries to match the given patterns starting from the current character,
        returns at the first matched pattern, if any, and advances the current
        character index by the length of the matched pattern
        :param patterns: string patterns
        :type patterns: str
        :return: if any pattern is matched returns the pattern string,
            otherwise returns None
        :rtype: Optional[str]
        """
        for pattern in patterns:
            if self.source.startswith(pattern, self.current):
                self.advance(len(pattern))
                return pattern
        return None

    def current_lexeme(self) -> str:
        """
        Returns the currently selected lexeme
        :return:
            the string between the lexeme start and
            the current character
        :rtype: str
        """
        return self.source[self.lexeme_start:self.current]

    def capture(self, token_type: TokenType, value: Any = None) -> None:
        """
        Captures the currently selected lexeme to a token and appends it to the
        token list.
        Ex:
        >>> lexer = BaseLexer('x = 2')
        >>> lexer.match('x')
        'x'
        >>> lexer.capture(TokenType.IDENTIFIER)
        :param token_type:
        :type token_type:
        :param value:
        :type value:
        :rtype: None
        """
        token = Token[TokenType](token_type, self.current_lexeme(), self.here(), value)
        self.sync()
        assert token
        self.tokens.append(token)

    def new_line(self) -> None:
        """
        Increases the line counter and syncs the line start with the current character
        :rtype: None
        """
        self.line += 1
        self.line_start = self.current

    @abstractmethod
    def next_token(self) -> None:
        """
        Mus be implemented in subclasses so the lexer can analyse the next token
        :rtype: None
        """
        pass

    def tokenize(self) -> List[Token[TokenType]]:
        """
        Lexer's main loop
        :return: List containing the tokens after lexing
        :rtype: List[Token[TokenType]]
        """
        while not self.is_at_end:
            self.next_token()
        return self.tokens
