from typing import FrozenSet, Dict, Set, List, Optional
from dataclasses import dataclass
from graphviz import Digraph
import os
from itertools import filterfalse


@dataclass
class NFA:
    initial: str
    states: FrozenSet[str]
    finals: FrozenSet[str]
    transitions: Dict[str, Dict[str, FrozenSet[str]]]

    def epsilon_closure(self, state: str)->Set[str]:
        if state not in self.states:
            raise ValueError(f"the state '{state}' doesn't belong to this NFA")
        closure = set()
        pending = [state]
        while pending:
            current = pending.pop()
            closure.add(current)
            pending.extend(filterfalse(lambda x: x in closure,
                                       self.transitions.get(current, {}).get('', frozenset())))
        return closure

    def determinize(self):
        initial = frozenset(self.epsilon_closure(self.initial))

        pass


