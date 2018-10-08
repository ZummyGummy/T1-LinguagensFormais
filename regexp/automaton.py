from typing import FrozenSet, Dict, Set, List
from .parser import RegexNode, RegexVisitor, Term, Concat, Option, EndMarker, Choice, Star
from automata import DFA


class RegexToDFA(RegexVisitor):
    def __init__(self):
        self.__term_count = 0
        self.__follow: Dict[int, FrozenSet[int]] = {}
        self.__terms: Dict[int, Term] = {}
        self.__symbols: Set[str] = set()

    def visit_term(self, node: Term, *args, **kwargs):
        idx = self.__term_count
        self.__terms[idx] = node
        self.__term_count += 1
        self.__follow[idx] = frozenset()
        if node is not EndMarker:
            self.__symbols.add(node.value)
        nullable = node.value == ''
        first_pos = frozenset() if nullable else frozenset({idx})
        last_pos = frozenset() if nullable else frozenset({idx})
        return nullable, first_pos, last_pos

    def visit_concat(self, node: Concat, *args, **kwargs):
        lhs_null, fst_lhs, lst_lhs = self.visit(node.lhs)
        rhs_null, fst_rhs, lst_rhs = self.visit(node.rhs)

        first_pos = (fst_lhs | fst_rhs) if lhs_null else fst_lhs
        last_pos = (lst_lhs | lst_rhs) if rhs_null else lst_rhs
        for term in lst_lhs:
            self.__follow[term] |= fst_rhs
        return lhs_null and rhs_null, first_pos, last_pos

    def visit_choice(self, node: Choice, *args, **kwargs):
        lhs_null, fst_lhs, lst_lhs = self.visit(node.lhs)
        rhs_null, fst_rhs, lst_rhs = self.visit(node.rhs)
        return lhs_null or rhs_null, (fst_lhs | fst_rhs), (lst_lhs | lst_rhs)

    def visit_option(self, node: Option, *args, **kwargs):
        _, fst_lhs, lst_lhs = self.visit(node.lhs)
        return True, fst_lhs, lst_lhs

    def visit_star(self, node: Star, *args, **kwargs):
        _, fst_lhs, lst_lhs = self.visit(node.lhs)
        for term in lst_lhs:
            self.__follow[term] |= fst_lhs
        return True, fst_lhs, lst_lhs

    def convert(self, node: RegexNode) -> DFA:
        def state_name(items: Set[int]) -> str:
            data = ', '.join(map(str, items))
            return f'{{{data}}}'
        _, first, last = self.visit(node)
        marked: Set[Set[int]] = set()
        pending: List[Set[int]] = [first, last]
        transitions = {}
        while pending:
            current = pending.pop()
            marked.add(current)
            transitions[state_name(current)] = {}
            for sym in self.__symbols:
                following = set()
                for index in current:
                    if self.__terms[index].value == sym:
                        following |= self.__follow[index]
                following = frozenset(following)
                if following:
                    transitions[state_name(current)][sym] = state_name(following)
                    if following not in marked:
                        pending.append(following)
        states = set(map(state_name, marked))
        final_index = self.__term_count - 1
        finals = set(map(state_name, filter(lambda s: final_index in s, marked)))
        automata = DFA()
        automata.transitions = transitions
        automata.states = states
        automata.finals = finals
        automata.set_alphabet()

        return automata
