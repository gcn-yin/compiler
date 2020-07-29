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

class NfaRulebook:
    def __init__(self, rules):
        self.rules = rules

    def follow_rules_for(self, state, character):
        return list(map(lambda x: x.follow(), self.rules_for(state, character)))

    def rules_for(self, state, character):
        return filter(lambda rule: rule.applies_to(state, character), self.rules)


def main():
    rulebook = NfaRulebook([
        FaRule(1, '1', 1), FaRule(1, 'b', 1), FaRule(1, 'b', 2)
    ])

if __name__ == '__main__':
    main()