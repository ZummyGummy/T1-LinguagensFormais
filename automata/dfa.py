from typing import FrozenSet, Dict, Set, List, Optional
from dataclasses import dataclass
from graphviz import Digraph
import os
from itertools import filterfalse


@dataclass
class DFA:
    initial: str
    states: FrozenSet[str]
    finals: FrozenSet[str]
    transitions: Dict[str, Dict[str, str]]

    def render(self, filename: Optional[os.PathLike]=None):
        graph = Digraph(format='svg')
        graph.node('initial', shape='point')
        for state in self.finals:
            graph.node(state, state, peripheries='2')
        for state in self.states - self.finals:
            graph.node(state, state)
        for src, trans in self.transitions.items():
            for sym, dest in trans.items():
                graph.edge(src, dest, sym)
        graph.edge('initial', self.initial)
        graph.render(filename=filename)

    def remove_dead(self) -> 'DFA':
        alive = frozenset(filter(self.transitions.get, self.transitions.keys()))
        if self.initial not in alive:
            return DFA(self.initial, frozenset(), frozenset(), {})
        trans = {
            src: {
                sym: dest for sym, dest in sc.items() if dest in alive
            } for src, sc in self.transitions.items()
        }
        return DFA(self.initial, alive, alive & self.finals, trans)

    def remove_unreachable(self) -> 'DFA':
        reachable = set()
        pending = [self.initial]
        while pending:
            current = pending.pop()
            reachable.add(current)
            succ = self.transitions[current].values()
            pending.extend(filterfalse(lambda x: x in reachable, succ))
        trans = {
            src: {
                sym: dest for sym, dest in sc.items() if dest in reachable
            } for src, sc in self.transitions.items() if src in reachable
        }
        return DFA(self.initial, frozenset(reachable), frozenset(reachable & self.finals), trans)

    def minimize(self) -> 'DFA':
        dfa = self.remove_dead().remove_unreachable()


    def __add__(self, other):
        pass
        # if not isinstance(other, DFA):
        #     raise ValueError('cannot concat ')
