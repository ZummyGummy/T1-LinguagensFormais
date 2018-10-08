from typing import FrozenSet, Dict, Set, List, Optional
from dataclasses import dataclass
from graphviz import Digraph
import os
from itertools import filterfalse


class DFA(object):

    def __init__(self):
        self.name = ""
        self.initials = ""
        self.alphabet = set()
        self.states = []
        self.finals = []
        self.transitions = {}

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

    def set_name(self, name):
        self.name = name

    def remove_dead(self):
        vivos = {x for x in self.finals}
        aux_vivos = set()
        while vivos != aux_vivos:
            aux_vivos = {x for x in vivos}
            for s in self.states:
                if s in self.transitions.keys():
                    for a in self.transitions[s].keys():
                        if self.transitions[s][a] in aux_vivos:
                            vivos.add(s)
        # remover estados mortos
        states = [x for x in self.states]
        for st in states:
            if st not in vivos:
                self.delete_state(st)

    def alphabet(self) -> Set[str]:
        syms = set()
        for trans in self.transitions.values():
            syms |= set(trans.keys())
        return syms

    def remove_unacess(self):
        acessiveis = set()
        acessiveis.add(self.initials)
        aux_acessiveis = set()
        while acessiveis != aux_acessiveis:
            aux_acessiveis = {x for x in acessiveis}
            for s in aux_acessiveis:
                if s in self.transitions.keys():
                    for a in self.transitions[s].keys():
                        acessiveis.add(self.transitions[s][a])
        # remover estados inacessiveis
        states = [x for x in self.states]
        for st in states:
            if st not in acessiveis:
                self.delete_state(st)

    def create_state(self, name, initial, final):
        if not self.verify_name(name):
            if initial:
                self.initials = name
            if final:
                self.finals.append(name)
            self.states.append(name)

    def delete_state(self, name):
        if name not in self.states:
            print("state not found")
            return
        self.states.remove(name)
        if name in self.transitions.keys():
            del self.transitions[name]
        states = list(self.transitions.keys())
        for q in states:
            keys = list(self.transitions[q].keys())
            for key in keys:
                if self.transitions[q][key] is name:
                    del self.transitions[q][key]
        self.update_alphabet()
        if name == self.initials:
            self.initials = ""
        if name in self.finals:
            self.finals.remove(name)

    def update_alphabet(self):
        new_alphabet = set()
        for q in self.transitions.keys():
            for k in self.transitions[q].keys():
                if k not in new_alphabet:
                    new_alphabet.add(k)
        self.alphabet = {x for x in new_alphabet}

    def minimize(self) -> 'DFA':
        dfa = self.remove_dead().remove_unreachable()

    def set_alphabet(self, alphabet):
        for char in alphabet:
            self.alphabet.append(char)

    def __add__(self, other):
        if other not in self.alphabet:
            self.alphabet.append(other)

    def add_transition(self, state, other):
        if state not in self.alphabet:
            return 0
        transition = dict[state, dict[state, other]]
        self.transitions.update(transition);

    def create_transition(self, name_state1, name_state2, key):
        name1 = name_state1
        name2 = name_state2
        if name1 not in self.states:
            if not self.verify_name(name_state1):
                self.create_state(name_state1, False, False)
            else:
                name1 = self.equi_name(name_state1)
        if name2 not in self.states:
            if not self.verify_name(name_state2):
                self.create_state(name_state2, False, False)
            else:
                name2 = self.equi_name(name_state2)
        self.create_transition_aux(name1)
        if key in self.transitions[name1].keys():
            split = set(self.transitions[name1][key].split(', '))
            name_state2_split = set(name2.split(', '))
            simmetric_diff = name_state2_split ^ split
            for d in simmetric_diff:
                if d not in split:
                    self.transitions[name1][key] += ', ' + d
        else:
            self.transitions[name1][key] = name2
        if key not in self.alphabet:
            self.alphabet.add(key)

    def create_transition_aux(self, name):
        if name not in self.transitions.keys():
            self.transitions[name] = {}

    def verify_name(self, name):
        resultado = False
        avaliar = set(name.split(', '))
        for estado in self.states:
            estado_split = set(estado.split(', '))
            if avaliar ^ estado_split == set():
                resultado = True
            if resultado:
                break
        return resultado

    def equi_name(self, name):
        resultado = False
        avaliar = set(name.split(', '))
        for estado in self.states:
            estado_split = set(estado.split(', '))
            if avaliar ^ estado_split == set():
                resultado = True
            if resultado:
                break
        return estado

    def add_initial(self, name_state):
        self.initials = name_state

    def add_final(self, name_state):
        if self.verify_name(name_state):
            name = self.equi_name(name_state)
            if name not in self.finals:
                self.finals.append(name)

    def delete_all_transitions(self, name_state, key):
        if name_state not in self.transitions.keys():
            print("state not found")
            return
        state_keys = list(self.transitions[name_state])
        if key not in state_keys:
            print("key not found")
            return
        del self.transitions[name_state][key]
        self.calculate_alphabet()