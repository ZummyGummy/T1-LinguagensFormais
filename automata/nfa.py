from typing import FrozenSet, Dict, Set, List, Optional
from dataclasses import dataclass
from graphviz import Digraph
import os
from itertools import filterfalse


class NFA(object):

    def __init__(self):
        self.name = ""
        self.initial = ""
        self.alphabet = []
        self.states = []
        self.finals = []
        self.transitions = {}

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

    def alphabet(self) -> Set[str]:
        syms = set()
        for trans in self.transitions.values():
            syms |= set(trans.keys())
        return syms

    def determinize(self):
        initial = frozenset(self.epsilon_closure(self.initial))

        pass

    def set_name(self, name):
        self.name = name;


