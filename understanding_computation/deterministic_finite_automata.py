class FaRule:
    def __init__(self, state, character, next_state):
        self.state = state
        self.character = character
        self.next_state = next_state

    def applies_to(self, state, character):
        return self.state == state and self.character == character

    def follow(self):
        return self.next_state

    def __str__(self):
        return "<FaRule: " + str(self.state) + "--" + str(self.character) + "-->" + str(self.next_state)

class DfaRuleBook:
    def __init__(self, rules):
        self.rules = rules

    def next_state(self, state, character):
        return self.rule_for(state, character).follow()

    def rule_for(self, state, character):
        result = list(filter(lambda rule: rule.applies_to(state, character), self.rules))[0]
        return result

class Dfa:
    def __init__(self, current_state, accept_states, rulebook):
        self.current_state = current_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepting(self):
        return self.current_state in self.accept_states

    def read_character(self, character):
        self.current_state = self.rulebook.next_state(self.current_state, character)

    def read_string(self, string):
        for char in string:
            self.read_character(char)


class DfaDesign:
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def to_dfa(self):
        return Dfa(self.start_state, self.accept_states, self.rulebook)

    def accepts(self, string):
        dfa = self.to_dfa()
        dfa.read_string(string)
        return dfa.accepting()

from collections import Iterable 

def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x

def accumulate(list_object):
    result = []
    for i in list_object:
        if not isinstance(i, list):
            result.append(i)
        if isinstance(i, list):
            result.extend(accumulate(i))
    return result

def flat_map(f, item):
    return map(f, flatten(item))

class NfaRulebook:
    def __init__(self, rules):
        self.rules = rules

    def next_states(self, states, character):
        return set(accumulate(list(flat_map(lambda state: self.follow_rules_for(state, character), 
                                            states))))
                
    def follow_rules_for(self, state, character):
        return list(map(lambda x: x.follow(), self.rules_for(state, character)))

    def rules_for(self, state, character):
        return filter(lambda rule: rule.applies_to(state, character), self.rules)

    def follow_free_moves(self, states):
        more_states = self.next_states(states, None)
        if more_states.issubset(states):
            return states
        else:
            return self.follow_free_moves(states | more_states)

class Nfa:
    def __init__(self, current_states, accept_states, rulebook):
        self.accept_states = accept_states
        self.rulebook = rulebook
        self.current_states = self.rulebook.follow_free_moves(set(current_states))

    def accepting(self):
        return bool(len(set(self.current_states) & set(self.accept_states)) != 0)

    def read_character(self, character):
        self.current_states = self.rulebook.next_states(self.current_states, character)

    def read_string(self, string):
        for char in string:
            self.read_character(char)

class NfaDesign:
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepts(self, string):
        nfa = self.to_nfa()
        nfa.read_string(string)
        return nfa.accepting()

    def to_nfa(self):
        return Nfa(self.start_state, self.accept_states, self.rulebook)

def main():
    rulebook = NfaRulebook([
        FaRule(1, None, 2), FaRule(1, None, 4),
        FaRule(2, 'a', 3), FaRule(3, 'a', 2),
        FaRule(4, 'a', 5), FaRule(5, 'a', 6),
        FaRule(6, 'a', 4)
    ])
    nfa_design = NfaDesign(1, [2, 4], rulebook)
    print(nfa_design.accepts('aa'))
    print(nfa_design.accepts('aaa'))
    print(nfa_design.accepts('aaaaa'))

if __name__ == '__main__':
    main()