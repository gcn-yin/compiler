class FARule {
  constructor(public readonly state: number, public readonly character: string, public readonly nextState: number) {}

  public applyTo(state: number, character: string) {
    return this.state === state && this.character === character;
  }
}

class DFARuleBook {
  constructor(public readonly rules: Array<FARule>) {}

  public nextState(state: number, character: string) {
    return this.ruleFor(state, character)?.nextState;
  }

  public ruleFor(state: number, character: string) {
    for (const rule of this.rules) {
      if (rule.applyTo(state, character)) {
        return rule;
      }
    }
  }
}

class DFA {
  constructor(
    public currentState: number,
    public readonly acceptStates: Array<number>,
    public readonly ruleBook: DFARuleBook
  ) {}

  public accepting() {
    return this.acceptStates.includes(this.currentState);
  }

  public readCharacter(character: string) {
    this.currentState = this.ruleBook.nextState(this.currentState, character) || -1;
  }

  public readString(s: string) {
    for (const char of s) {
      this.readCharacter(char);
    }
  }
}

class DFADesign {
  constructor(public startState: number, public acceptStates: Array<number>, public readonly ruleRook: DFARuleBook) {}

  public toDfa() {
    return new DFA(this.startState, this.acceptStates, this.ruleRook);
  }

  public accepts(s: string) {
    const dfa = this.toDfa();
    dfa.readString(s);
    return dfa.accepting();
  }
}

const ruleBook = new DFARuleBook([
  new FARule(1, "a", 2),
  new FARule(1, "b", 1),
  new FARule(2, "a", 2),
  new FARule(2, "b", 3),
  new FARule(3, "a", 3),
  new FARule(3, "b", 3),
]);

class NFARuleBook {
  constructor(public readonly rules: Array<FARule>) {}

  public nextStates(states: Set<number>, character: string) {
    const s = Array.from(states);
    return new Set<number>(s.flatMap((state) => this.followRulesFor(state, character)));
  }

  public followRulesFor(state: number, character: string) {
    return this.rulesFor(state, character).map((rule) => rule.nextState);
  }

  public rulesFor(state: number, character: string) {
    return this.rules.filter((rule) => rule.applyTo(state, character));
  }
}

console.log(ruleBook.nextState(1, "a"));
console.log(ruleBook.nextState(1, "b"));
console.log(ruleBook.nextState(2, "b"));

const dfa = new DFA(1, [3], ruleBook);
console.log(dfa.accepting());
dfa.readString("baaab");
console.log(dfa.accepting());

const dfaDesign = new DFADesign(1, [3], ruleBook);
console.log(dfaDesign.accepts("a"));
console.log(dfaDesign.accepts("baa"));
console.log(dfaDesign.accepts("baba"));

const nfaRuleBook = new NFARuleBook([
  new FARule(1, "a", 1),
  new FARule(1, "b", 1),
  new FARule(1, "b", 2),
  new FARule(2, "a", 3),
  new FARule(2, "b", 3),
  new FARule(3, "a", 4),
  new FARule(3, "b", 4),
]);

console.log(nfaRuleBook.nextStates(new Set([1]), "b"));
console.log(nfaRuleBook.nextStates(new Set([1, 2]), "a"));

class NFA {
  constructor(
    public currentStates: Set<number>,
    public acceptStates: Set<number>,
    public readonly ruleBook: NFARuleBook
  ) {}

  public accepting() {
    const c = Array.from(this.currentStates);
    const a = Array.from(this.acceptStates);
    const intersectionLength = c.filter((it) => a.includes(it)).length;
    return intersectionLength > 0;
  }

  public readCharacter(character: string) {
    this.currentStates = this.ruleBook.nextStates(this.currentStates, character);
  }

  public readString(s: string) {
    for (const char of s) {
      this.readCharacter(char);
    }
  }
}

console.log("NFA -------------------");
console.log(new NFA(new Set([1]), new Set([4]), nfaRuleBook).accepting());
console.log(new NFA(new Set([1, 2, 4]), new Set([4]), nfaRuleBook).accepting());

let nfa = new NFA(new Set([1]), new Set([4]), nfaRuleBook);
console.log(nfa.accepting());
nfa.readCharacter("b");
console.log(nfa.accepting());
nfa.readCharacter("a");
console.log(nfa.accepting());
nfa.readCharacter("b");
console.log(nfa.accepting());
nfa = new NFA(new Set([1]), new Set([4]), nfaRuleBook);
nfa.readString("bbbbb");
console.log(nfa.accepting());

class NFADesign {
  constructor(
    public readonly startState: number,
    public readonly acceptStates: Set<number>,
    public readonly ruleBook: NFARuleBook
  ) {}

  public accepts(s: string) {
    const nfa = this.toNfa();
    nfa.readString(s);
    return nfa.accepting();
  }

  public toNfa() {
    return new NFA(new Set([this.startState]), this.acceptStates, this.ruleBook);
  }
}

console.log("NFADesign ------------------");
const nfaDesign = new NFADesign(1, new Set([4]), nfaRuleBook);
console.log(nfaDesign.accepts("bab"));
console.log(nfaDesign.accepts("bbbbb"));
console.log(nfaDesign.accepts("bbabb"));
