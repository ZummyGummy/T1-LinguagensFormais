from regexp.parser import RegexParser, RegexNode
from regexp.automaton import RegexToDFA


def to_ast(source: str) -> RegexNode:
    parser = RegexParser()
    tree = parser.parse(source)
    return tree

#
# def printer_test(source: str) -> str:
#     tree = to_ast(source)
#     pr = BRegexPrinter()
#     return pr.print(tree)

#
# def thread(source: str) -> BasicRegex:
#     tree = to_ast(source)
#     tr = BRegexThreader()
#     tr.visit(tree)
#     return tree


def render(source: str) -> None:
    tree = to_ast(source)
    converter = RegexToDFA()
    dfa = converter.convert(tree)
    dfa.render()
